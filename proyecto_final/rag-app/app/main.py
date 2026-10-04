from fastapi import FastAPI
from pydantic import BaseModel
from app.store import VectorStore
from app.embed import EmbeddingClient
from app.generate import ResponseGenerator
from app.chunk import chunk_file
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
app = FastAPI(title="RAG System API", version="1.0")

# Initialize vector store and clients

store = VectorStore(persist_dir = "chroma")
# Both clients read GOOGLE_API_KEY from the environment
try:
    embed_client = EmbeddingClient()
    response_gen = ResponseGenerator(min_score = 0.3)
except ValueError:
    embed_client = None
    response_gen = None

# Models

class Chunk(BaseModel):
    id: int
    source: str
    text: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    citations: list[Chunk]
    abstained: bool

class IngestRequest(BaseModel):
    directory_path: str

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

class DocumentInfo(BaseModel):
    name: str

class DocumentsResponse(BaseModel):
    documents: list[DocumentInfo]

# Endpoints

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"api_configured": embed_client is not None}

@app.post("/ingest")
def ingest(request: IngestRequest):
    """Ingest documents into the vector store."""
    if not embed_client:
        return {"error": "API de Google AI no configurada", "status": "error"}
    
    all_chunks = []
    dir_path = Path(request.directory_path)
    file_paths = list(dir_path.glob("*.md")) + list(dir_path.glob("*.txt")) + list(dir_path.glob("*.pdf"))

    if not file_paths:
        return {"error": "No se encontraron archivos", "status": "error"}

    for filepath in file_paths:
        try:
            chunks = chunk_file(str(filepath), chunk_size = 300, overlap = 50)
            all_chunks.extend(chunks)
        except Exception as e:
            return {"error": f"Error al procesar {filepath}: {str(e)}", "status": "error"}
    
    if not all_chunks:
        return {"error": "No se generaron chunks", "status": "error"}

    try:
        texts_to_embed = [chunk["text"] for chunk in all_chunks]
        embeddings = embed_client.embed_batch(texts_to_embed)
        store.add_chunks(all_chunks, embeddings)
        return {"status": "success"}
    except Exception as e:
        return {"error": f"Error al guardar documentos: {str(e)}", "status": "error"}

@app.post("/query")
def query(request: QueryRequest) -> QueryResponse:
    """Query the RAG system."""
    if not embed_client or not response_gen:
        return QueryResponse(
            answer = "API de Google AI no configurada",
            citations = [],
            abstained = True
        )
    
    if not request.question or len(request.question.strip()) == 0:
        return QueryResponse(
            answer = "Por favor escribe una pregunta",
            citations = [],
            abstained = True
        )

    try:
        query_embedding = embed_client.embed_query(request.question)
    except Exception as e:
        return QueryResponse(
            answer = f"Error al generar embedding de la consulta: {str(e)}",
            citations = [],
            abstained = True
        )

    try:
        chunks = store.search(query_embedding, top_k = request.top_k)
    except Exception as e:
        return QueryResponse(
            answer = f"Error al recuperar documentos: {str(e)}",
            citations = [],
            abstained = True
        )

    used_chunks = []
    try:
        gen_result = response_gen.generate(request.question, chunks)
        answer = gen_result["answer"]
        abstained = gen_result["abstained"]
        used_chunks = gen_result["citations"]
    except Exception as e:
        answer = f"Error al generar respuesta: {str(e)}"
        abstained = True

    # Only cite the chunks actually given to the model
    citations = [
        Chunk(id = c["id"], source = c["source"], text = c["text"], score = round(c["score"], 4))
        for c in used_chunks
    ]
    
    return QueryResponse(
        answer = answer,
        citations = citations,
        abstained = abstained
    )

@app.get("/documents", response_model = DocumentsResponse)
def get_documents():
    return store.get_documents()

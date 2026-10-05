from typing import Annotated
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, StringConstraints
from app.store import VectorStore
from app.embed import EmbeddingClient
from app.generate import ResponseGenerator
from app.chunk import chunk_file
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
app = FastAPI(title="API Sistema RAG", version="1.0")

store = VectorStore(persist_dir = "chroma")
# Ambos clientes leen GOOGLE_API_KEY del entorno
try:
    embed_client = EmbeddingClient()
    response_gen = ResponseGenerator(min_score = 0.3)
except ValueError:
    embed_client = None
    response_gen = None

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
    question: Annotated[str, StringConstraints(strip_whitespace = True, min_length = 1)]
    top_k: int = Field(default = 3, ge = 1)

class DocumentInfo(BaseModel):
    name: str

class DocumentsResponse(BaseModel):
    documents: list[DocumentInfo]

def require_api_configured() -> None:
    if not embed_client or not response_gen:
        raise HTTPException(status_code = 503, detail = "API de Google AI no configurada")

@app.get("/health")
def health():
    """Indica si la API de Google AI está configurada."""
    return {"api_configured": embed_client is not None}

@app.post("/ingest")
def ingest(request: IngestRequest):
    """Carga los documentos de un directorio en la base vectorial."""
    require_api_configured()

    dir_path = Path(request.directory_path)
    file_paths = list(dir_path.glob("*.md")) + list(dir_path.glob("*.txt")) + list(dir_path.glob("*.pdf"))
    if not file_paths:
        raise HTTPException(
            status_code = 404,
            detail = f"No se encontraron archivos .md, .txt o .pdf en '{request.directory_path}'"
        )

    all_chunks = []
    for filepath in file_paths:
        try:
            all_chunks.extend(chunk_file(str(filepath), chunk_size = 300, overlap = 50))
        except Exception:
            raise HTTPException(status_code = 422, detail = f"No se pudo procesar {filepath.name}")

    if not all_chunks:
        raise HTTPException(status_code = 422, detail = "Los archivos no contienen texto")

    try:
        embeddings = embed_client.embed_batch([chunk["text"] for chunk in all_chunks])
    except Exception:
        raise HTTPException(status_code = 502, detail = "Error al generar los embeddings con Google AI")

    try:
        store.add_chunks(all_chunks, embeddings)
    except Exception:
        raise HTTPException(status_code = 500, detail = "Error al guardar los documentos")

    return {"status": "success"}

@app.post("/query")
def query(request: QueryRequest) -> QueryResponse:
    """Responde una pregunta usando los documentos cargados."""
    require_api_configured()

    try:
        query_embedding = embed_client.embed_query(request.question)
    except Exception:
        raise HTTPException(status_code = 502, detail = "Error al generar el embedding de la pregunta")

    try:
        chunks = store.search(query_embedding, top_k = request.top_k)
    except Exception:
        raise HTTPException(status_code = 500, detail = "Error al recuperar documentos")

    try:
        gen_result = response_gen.generate(request.question, chunks)
    except Exception:
        raise HTTPException(status_code = 502, detail = "Error al generar la respuesta con Gemini")

    # Solo se citan los chunks que recibió el modelo
    citations = [
        Chunk(id = c["id"], source = c["source"], text = c["text"], score = round(c["score"], 4))
        for c in gen_result["citations"]
    ]

    return QueryResponse(
        answer = gen_result["answer"],
        citations = citations,
        abstained = gen_result["abstained"]
    )

@app.get("/documents", response_model = DocumentsResponse)
def get_documents():
    """Lista los documentos cargados."""
    return store.get_documents()
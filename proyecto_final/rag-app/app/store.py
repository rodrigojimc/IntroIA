import chromadb
from pathlib import Path
from typing import List, TypedDict
from app.chunk import TextChunk


class RetrievedChunk(TypedDict):
    """Chunk devuelto por una búsqueda de similitud."""
    id: int
    chunk_id: str
    source: str
    text: str
    score: float

class DocumentEntry(TypedDict):
    name: str

class DocumentsResult(TypedDict):
    documents: List[DocumentEntry]

class VectorStore:
    """Base vectorial persistente sobre ChromaDB."""
    
    def __init__(self, persist_dir: str = "chroma"):
        Path(persist_dir).mkdir(parents = True, exist_ok = True)

        self.client = chromadb.PersistentClient(path = persist_dir)

        self.collection = self.client.get_or_create_collection(
            name = "rag_documents",
            metadata = {"hnsw:space": "cosine"}
        )
    
    def add_chunks(
        self,
        chunks: List[TextChunk],
        embeddings: List[List[float]]
    ) -> None:
        ids = [chunk["id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadata = [
            {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"]
            }
            for chunk in chunks
        ]
        
        self.collection.add(
            ids = ids,
            embeddings = embeddings,
            documents = documents,
            metadatas = metadata
        )
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 3
    ) -> List[RetrievedChunk]:
        """Devuelve los top_k chunks más similares a la consulta."""

        results = self.collection.query(
            query_embeddings = [query_embedding],
            n_results = top_k,
            include = ["documents", "metadatas", "distances"]
        )

        chunks: List[RetrievedChunk] = []
        if results["ids"]:
            for idx, (chunk_id, document, metadata, distance) in enumerate(zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )):

                # Chroma devuelve distancia coseno (0 = idéntico, 2 = opuesto); se convierte a similitud
                similarity_score = 1 - distance
                
                chunks.append({
                    "id": idx + 1,
                    "chunk_id": chunk_id,
                    "source": metadata["source"],
                    "text": document,
                    "score": similarity_score
                })
        
        return chunks
    
    def get_documents(self) -> DocumentsResult:
        """Devuelve los nombres de los documentos cargados, sin repetir."""
        results = self.collection.get(include = ["metadatas"])

        sources: set[str] = set()
        for metadata in results["metadatas"] or []:
            sources.add(str(metadata.get("source", "Desconocido")))

        documents = [DocumentEntry(name=name) for name in sorted(sources)]

        return {"documents": documents}

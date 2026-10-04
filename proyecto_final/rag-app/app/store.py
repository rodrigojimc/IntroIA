import chromadb
from pathlib import Path
from typing import List, TypedDict
from app.chunk import TextChunk


class RetrievedChunk(TypedDict):
    """A chunk returned by a similarity search."""
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
    """ChromaDB vector store wrapper."""
    
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
        """Add chunks to the store."""
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
        """Search for similar documents."""

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

                # ChromaDB returns distances, where 0 is identical and 2 is completely different
                # Convert distance to similarity score (cosine distance to similarity)
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
        """Get list of unique documents in the collection."""
        results = self.collection.get(include = ["metadatas"])

        sources: set[str] = set()
        for metadata in results["metadatas"] or []:
            sources.add(str(metadata.get("source", "Unknown")))

        documents = [DocumentEntry(name=name) for name in sorted(sources)]

        return {"documents": documents}

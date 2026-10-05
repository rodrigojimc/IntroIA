import os
from typing import List
import google.generativeai as genai


class EmbeddingClient:
    """Cliente de embeddings de Google AI."""
    
    def __init__(self, api_key: str = None, model: str = "gemini-embedding-001"):
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no está definida")
        
        genai.configure(api_key = api_key)
        self.model = model
    
    def embed(self, text: str) -> List[float]:
        response = genai.embed_content(
            model = self.model,
            content = text,
            task_type = "RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            embedding = self.embed(text)
            embeddings.append(embedding)
        return embeddings
    
    def embed_query(self, query: str) -> List[float]:
        response = genai.embed_content(
            model = self.model,
            content = query,
            task_type = "RETRIEVAL_QUERY"
        )
        return response['embedding']

import os
from typing import List, TypedDict
import google.generativeai as genai
from app.store import RetrievedChunk


class GenerationResult(TypedDict):
    answer: str
    abstained: bool
    citations: List[RetrievedChunk]

ABSTAIN_MESSAGE = "No tengo suficiente evidencia en los documentos para responder esta pregunta."

class ResponseGenerator:
    def __init__(self, api_key: str = None, model: str = "gemini-pro-latest", min_score: float = 0.3):
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set in environment or passed as argument")
        
        genai.configure(api_key = api_key)
        self.model_name = model
        self.min_score = min_score
    
    def generate(
        self,
        question: str,
        chunks: List[RetrievedChunk]
    ) -> GenerationResult:
        """Generate a response ground"""
        abstain: GenerationResult = {"answer": ABSTAIN_MESSAGE, "abstained": True, "citations": []}

        # Keep only chunks above the threshold; abstain if none qualify
        relevant_chunks = [c for c in chunks if c["score"] >= self.min_score]
        if not relevant_chunks:
            return abstain

        relevant_chunks = [
            RetrievedChunk(id = i, chunk_id = c["chunk_id"], source = c["source"], text = c["text"], score = c["score"])
            for i, c in enumerate(relevant_chunks, 1)
        ]

        context_text = ""
        for chunk in relevant_chunks:
            context_text += f"[{chunk['id']}] (Fuente: {chunk['source']})\n"
            context_text += f"{chunk['text']}\n\n"
        
        # Create prompt that enforces grounded generation
        prompt = f"""Eres un asistente de IA que responde preguntas basándote ÚNICAMENTE en la información proporcionada.

Contexto basado en los siguientes documentos:

{context_text}

Pregunta: {question}

Instrucciones:
- Responde en español.
- Responde ÚNICAMENTE usando la información en los documentos anteriores.
- Incluye citas [1], [2], etc. refiriéndote a los documentos numerados.
- Si la pregunta no puede responderse con los documentos proporcionados, responde exactamente y solo: "{ABSTAIN_MESSAGE}".
- No agregues información externa o conocimiento general.
- Sé conciso y directo.

Respuesta:"""
        
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            
            if response.text:
                answer = response.text.strip()

                if "no tengo suficiente evidencia" in answer.lower():
                    return abstain

                return {
                    "answer": answer,
                    "abstained": False,
                    "citations": relevant_chunks
                }
            else:
                return {
                    "answer": "No pude generar una respuesta. Intenta reformular la pregunta.",
                    "abstained": True,
                    "citations": []
                }

        except Exception as e:
            return {
                "answer": f"Error generando respuesta: {str(e)}",
                "abstained": True,
                "citations": []
            }

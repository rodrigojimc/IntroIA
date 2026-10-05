"""División de documentos en chunks con solapamiento."""
import re
from typing import List, TypedDict
import os
from pathlib import Path


class TextChunk(TypedDict):
    id: str
    text: str
    source: str
    chunk_index: int

def split_into_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def count_tokens_simple(text: str) -> int:
    return len(text.split())

def chunk_text(
    text: str,
    chunk_size: int = 300,
    overlap: int = 50,
    source: str = "desconocido"
) -> List[TextChunk]:
    """Divide el texto en chunks de unas chunk_size palabras que se solapan unas overlap palabras."""
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []
    current_tokens = 0
    chunk_id = 0
    
    for sentence in sentences:
        sentence_tokens = count_tokens_simple(sentence)
        
        # Si la oración ya no cabe, se cierra el chunk actual
        if current_tokens + sentence_tokens > chunk_size and current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "id": f"{source}_chunk_{chunk_id}",
                "text": chunk_text,
                "source": source,
                "chunk_index": chunk_id
            })
            chunk_id += 1
            
            # El siguiente chunk empieza con las últimas oraciones del anterior para no perder contexto
            overlap_tokens = 0
            overlap_sentences = []
            for sent in reversed(current_chunk):
                overlap_tokens += count_tokens_simple(sent)
                overlap_sentences.insert(0, sent)
                if overlap_tokens >= overlap:
                    break
            
            current_chunk = overlap_sentences
            current_tokens = overlap_tokens
        
        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append({
            "id": f"{source}_chunk_{chunk_id}",
            "text": chunk_text,
            "source": source,
            "chunk_index": chunk_id
        })
    
    return chunks

def chunk_file(
    filepath: str,
    chunk_size: int = 300,
    overlap: int = 50
) -> List[TextChunk]:
    """Lee un archivo .txt, .md o .pdf y lo divide en chunks."""
    if filepath.lower().endswith('.pdf'):
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    else:
        text = Path(filepath).read_text(encoding = 'utf-8', errors = 'ignore')

    source = os.path.basename(filepath)
    
    return chunk_text(text, chunk_size = chunk_size, overlap = overlap, source = source)

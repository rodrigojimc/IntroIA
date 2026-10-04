"""Text chunking utilities for RAG."""
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
    source: str = "unknown"
) -> List[TextChunk]:
    """Split text into overlapping chunks."""
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []
    current_tokens = 0
    chunk_id = 0
    
    for sentence in sentences:
        sentence_tokens = count_tokens_simple(sentence)
        
        # If adding this sentence exceeds chunk_size, save current chunk
        if current_tokens + sentence_tokens > chunk_size and current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "id": f"{source}_chunk_{chunk_id}",
                "text": chunk_text,
                "source": source,
                "chunk_index": chunk_id
            })
            chunk_id += 1
            
            # Start overlap: keep last sentences to maintain context
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
    
    # Add final chunk
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
    """Read file and chunk its contents."""
    if filepath.lower().endswith('.pdf'):
        from pypdf import PdfReader
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    else:
        # .txt or .md
        text = Path(filepath).read_text(encoding = 'utf-8', errors = 'ignore')

    source = os.path.basename(filepath)
    
    return chunk_text(text, chunk_size = chunk_size, overlap = overlap, source = source)

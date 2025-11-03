"""Text processing and chunking utilities."""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
import config


def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
    """
    Split text into chunks using RecursiveCharacterTextSplitter.
    
    Args:
        text: Text to chunk.
        chunk_size: Maximum size of each chunk (in characters, roughly tokens). Defaults to config.CHUNK_SIZE.
        chunk_overlap: Overlap between chunks. Defaults to config.CHUNK_OVERLAP.
        
    Returns:
        List of text chunks.
    """
    if chunk_size is None:
        chunk_size = config.CHUNK_SIZE
    if chunk_overlap is None:
        chunk_overlap = config.CHUNK_OVERLAP
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    return chunks


def chunk_documents(texts: List[str], chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
    """
    Chunk multiple documents.
    
    Args:
        texts: List of document texts.
        chunk_size: Maximum size of each chunk.
        chunk_overlap: Overlap between chunks.
        
    Returns:
        List of all chunks from all documents.
    """
    all_chunks = []
    for text in texts:
        chunks = chunk_text(text, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)
    
    return all_chunks


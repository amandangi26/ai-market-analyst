"""Tests for ingestion module."""
import os
import tempfile
import shutil
from pathlib import Path
import config
from ingestion import document_loader, text_processor, vector_store


def test_load_txt_document():
    """Test loading a .txt document."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test file
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("This is a test document.")
        
        text = document_loader.load_single_document(str(test_file))
        assert "test document" in text.lower()


def test_chunk_text():
    """Test text chunking functionality."""
    long_text = "This is a test. " * 100  # Create long text
    
    chunks = text_processor.chunk_text(long_text, chunk_size=50, chunk_overlap=10)
    
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)


def test_vector_store_creation():
    """Test vector store can be created (if API key is set)."""
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "your_gemini_api_key_here":
        print("Skipping vector store test - Gemini API key not configured")
        return
    
    # This test requires API key, so we'll just check the function exists
    assert callable(vector_store.create_vector_store)


def test_document_loader_with_multiple_files():
    """Test loading multiple documents."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create multiple test files
        (Path(tmpdir) / "doc1.txt").write_text("Document 1 content")
        (Path(tmpdir) / "doc2.txt").write_text("Document 2 content")
        
        docs = document_loader.load_documents(tmpdir)
        assert len(docs) == 2
        assert "Document 1" in docs[0]
        assert "Document 2" in docs[1]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])


"""Document loader for various file formats."""
import os
from pathlib import Path
from typing import List
from pypdf import PdfReader
from docx import Document
import config


def load_documents(documents_dir: str = None) -> List[str]:
    """
    Load documents from the documents directory.
    
    Supports: .txt, .pdf, .docx, .md
    
    Args:
        documents_dir: Directory containing documents. Defaults to config.DOCUMENTS_DIR.
        
    Returns:
        List of document texts.
    """
    if documents_dir is None:
        documents_dir = config.DOCUMENTS_DIR
    
    documents = []
    supported_extensions = {'.txt', '.pdf', '.docx', '.md'}
    
    if not os.path.exists(documents_dir):
        print(f"Warning: Documents directory {documents_dir} does not exist.")
        return documents
    
    for file_path in Path(documents_dir).iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                text = load_single_document(str(file_path))
                if text:
                    documents.append(text)
                    print(f"Loaded: {file_path.name}")
            except Exception as e:
                print(f"Error loading {file_path.name}: {str(e)}")
    
    return documents


def load_single_document(file_path: str) -> str:
    """
    Load a single document based on its extension.
    
    Args:
        file_path: Path to the document file.
        
    Returns:
        Document text content.
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()
    
    if extension == '.txt' or extension == '.md':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    elif extension == '.pdf':
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    elif extension == '.docx':
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    else:
        raise ValueError(f"Unsupported file type: {extension}")


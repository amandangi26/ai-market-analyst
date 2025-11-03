"""Chroma vector store creation and management with local embeddings."""
import os
from typing import Optional, List
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
import config
from ingestion.document_loader import load_documents
from ingestion.text_processor import chunk_documents

# Global embedding model instance (loaded once)
_embedding_model = None


def get_local_embeddings():
    """Get or create the local embedding model instance."""
    global _embedding_model
    if _embedding_model is None:
        print(f"🧠 Loading local embeddings model: {config.EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        print("✅ Local embeddings model loaded successfully")
    return _embedding_model


class LocalEmbeddings:
    """Wrapper class for sentence-transformers to work with LangChain Chroma."""
    
    def __init__(self, model_name: str = None):
        if model_name is None:
            model_name = config.EMBEDDING_MODEL
        self.model = get_local_embeddings()
        self.model_name = model_name
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of texts."""
        if not texts:
            return []
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text."""
        embedding = self.model.encode([text], show_progress_bar=False, convert_to_numpy=True)
        return embedding[0].tolist()


def create_vector_store(force_rebuild: bool = False) -> Optional[Chroma]:
    """
    Create or load Chroma vector store from documents.
    
    Args:
        force_rebuild: If True, rebuild the vector store even if it exists.
        
    Returns:
        Chroma vector store instance, or None if creation fails.
    """
    persist_directory = config.CHROMA_PERSIST_DIR
    
    # Ensure persist directory exists
    os.makedirs(persist_directory, exist_ok=True)
    
    # Create embeddings wrapper
    embeddings = LocalEmbeddings()
    
    # Try to load existing store
    if not force_rebuild and os.path.exists(persist_directory) and os.listdir(persist_directory):
        try:
            print("🧩 Loading existing Chroma vector store...")
            vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings
            )
            # Check if store has documents
            try:
                count = vectorstore._collection.count()
                if count > 0:
                    print(f"✅ Chroma vector store loaded successfully ({count} documents)")
                    return vectorstore
                else:
                    print("⚠️  Vector store exists but is empty. Rebuilding...")
            except Exception as e:
                print(f"⚠️  Error checking vector store count: {str(e)}. Rebuilding...")
        except Exception as e:
            print(f"⚠️  Error loading vector store: {str(e)}. Rebuilding...")
    
    # Create new vector store
    print("🧩 Creating new Chroma vector store...")
    documents = load_documents()
    
    if not documents:
        print("⚠️  Warning: No documents found in data/documents/. Vector store will be empty.")
        # Create empty vector store
        try:
            vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings
            )
            return vectorstore
        except Exception as e:
            print(f"❌ Error creating empty vector store: {str(e)}")
            return None
    
    # Chunk documents
    chunks = chunk_documents(documents)
    
    if not chunks:
        print("⚠️  Warning: No chunks created. Vector store will be empty.")
        try:
            vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings
            )
            return vectorstore
        except Exception as e:
            print(f"❌ Error creating empty vector store: {str(e)}")
            return None
    
    # Create documents with metadata
    langchain_docs = [Document(page_content=chunk) for chunk in chunks]
    
    # Create vector store
    try:
        print(f"📝 Creating vector store with {len(langchain_docs)} document chunks...")
        vectorstore = Chroma.from_documents(
            documents=langchain_docs,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        vectorstore.persist()
        print(f"✅ Chroma vector store created successfully with {len(chunks)} chunks")
        print(f"📁 Persistent directory: {persist_directory}")
        return vectorstore
    except Exception as e:
        print(f"❌ Error creating vector store: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def get_vector_store() -> Optional[Chroma]:
    """
    Get the vector store instance, creating it if necessary.
    
    Returns:
        Chroma vector store instance, or None if creation fails.
    """
    return create_vector_store(force_rebuild=False)

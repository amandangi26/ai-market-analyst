"""Configuration module for AI Market Analyst."""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Provider Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")  # Updated to latest stable

# Embedding Configuration (Local)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Vector Store Configuration
VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "chroma")

# Security & Processing
ENABLE_GUARDRAILS = os.getenv("ENABLE_GUARDRAILS", "True").lower() == "true"
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
VECTORSTORE_DIR = os.path.join(DATA_DIR, "vectorstore")
CHROMA_PERSIST_DIR = os.path.join(VECTORSTORE_DIR, "chroma_db")

# Ensure directories exist
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(VECTORSTORE_DIR, exist_ok=True)
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)

# Validation
if not GEMINI_API_KEY or GEMINI_API_KEY == "your_actual_gemini_key_here":
    print("⚠️  WARNING: GEMINI_API_KEY not configured. Please set it in .env file")
else:
    print("✅ Loaded GEMINI_API_KEY")


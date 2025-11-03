"""Main FastAPI application for AI Market Analyst."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.routes import router
import config
import logging
import os
from dotenv import load_dotenv

# Force-load .env from the current directory
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("🚀 Starting AI Market Analyst API...")
    
    # Log configuration
    logger.info(f"🤖 LLM Provider: {config.LLM_PROVIDER}")
    logger.info(f"🤖 LLM Model: {config.LLM_MODEL}")
    logger.info(f"🧠 Local Embeddings: {config.EMBEDDING_MODEL}")
    logger.info(f"🧩 Vector Store: {config.VECTOR_STORE_TYPE}")
    logger.info(f"🔒 Guardrails Enabled: {config.ENABLE_GUARDRAILS}")
    logger.info(f"📊 Chunk Size: {config.CHUNK_SIZE}, Overlap: {config.CHUNK_OVERLAP}")
    
    # Validate Gemini API key
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "your_actual_gemini_key_here":
        logger.error("❌ GEMINI_API_KEY not configured! Please set it in .env file")
        logger.error("   Get your API key from: https://aistudio.google.com/app/apikey")
    else:
        logger.info(f"✅ Loaded GEMINI_API_KEY")
        logger.info(f"🤖 LLM: {config.LLM_MODEL}")
    
    # Initialize local embeddings
    try:
        from ingestion.vector_store import get_local_embeddings
        logger.info(f"🧠 Loading local embeddings model: {config.EMBEDDING_MODEL}")
        get_local_embeddings()
        logger.info("✅ Local embeddings model loaded")
    except Exception as e:
        logger.warning(f"⚠️  Error loading embeddings: {str(e)}")
    
    # Initialize vector store
    try:
        from ingestion.vector_store import create_vector_store
        logger.info("🧩 Initializing Chroma vector store...")
        vectorstore = create_vector_store()
        if vectorstore:
            logger.info("✅ Vector store initialized successfully")
        else:
            logger.warning("⚠️  Vector store initialization returned None")
    except Exception as e:
        logger.error(f"❌ Vector store initialization error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    yield
    
    # Shutdown (if needed in future)
    logger.info("Shutting down AI Market Analyst API...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="AI Market Analyst API",
    description="RAG-based market analysis and document Q&A system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Market Analyst API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "qa": "/api/v1/qa",
            "summary": "/api/v1/summary",
            "extract": "/api/v1/extract",
            "auto": "/api/v1/auto"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


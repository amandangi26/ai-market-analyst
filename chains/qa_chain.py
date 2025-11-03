"""RAG-based Q&A chain implementation using Gemini and Chroma."""
from typing import Optional, Dict, List
from chains.gemini_helper import ask_gemini
import config
from ingestion.vector_store import get_vector_store


def answer_question(question: str) -> dict:
    """
    Answer a question using the RAG pipeline with Gemini.
    
    Args:
        question: The question to answer.
        
    Returns:
        Dictionary with 'answer' and 'source_documents' keys.
    """
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "your_actual_gemini_key_here":
        return {
            "answer": "Error: GEMINI_API_KEY not configured. Please set it in .env file",
            "source_documents": []
        }
    
    vectorstore = get_vector_store()
    if vectorstore is None:
        return {
            "answer": "Error: Vector store not available. Please ensure documents are loaded.",
            "source_documents": []
        }
    
    try:
        # Retrieve relevant documents
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        relevant_docs = retriever.get_relevant_documents(question)
        
        # Build context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Create prompt for Gemini
        prompt = f"""Use the following pieces of context to answer the question at the end.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer based on the context:"""
        
        # Get answer from Gemini
        answer = ask_gemini(prompt, temperature=0.7)
        
        # Format source documents
        source_documents = [
            {"page_content": doc.page_content[:200] + "..."} 
            for doc in relevant_docs[:3]  # Limit to top 3 sources
        ]
        
        return {
            "answer": answer,
            "source_documents": source_documents
        }
        
    except Exception as e:
        error_msg = f"Error processing question: {str(e)}"
        print(error_msg)
        return {
            "answer": error_msg,
            "source_documents": []
        }

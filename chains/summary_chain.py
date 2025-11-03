"""Summary chain for long text summarization using Gemini."""
from chains.gemini_helper import ask_gemini
from ingestion.text_processor import chunk_text
import config


def summarize_text(text: str, max_length: int = 500) -> str:
    """
    Summarize a long text using Gemini.
    
    Args:
        text: Text to summarize.
        max_length: Maximum length of the summary (in words).
        
    Returns:
        Summary text.
    """
    if not text or len(text.strip()) == 0:
        return "No text provided for summarization."
    
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "your_actual_gemini_key_here":
        return "Error: GEMINI_API_KEY not configured"
    
    try:
        # If text is short, use simple summarization
        if len(text) < 3000:
            prompt = f"""Summarize the following text in approximately {max_length} words.
Be concise and capture the key points.

Text:
{text}

Summary:"""
            
            summary = ask_gemini(prompt, temperature=0.3)
            return summary
        
        # For long texts, chunk and summarize each chunk, then combine
        chunks = chunk_text(text, chunk_size=3000, chunk_overlap=200)
        
        if not chunks:
            return "Error: Could not chunk text for summarization"
        
        # Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            prompt = f"""Write a concise summary of the following text chunk ({i+1}/{len(chunks)}):

{chunk}

Concise summary:"""
            summary = ask_gemini(prompt, temperature=0.3)
            chunk_summaries.append(summary)
        
        # Combine summaries
        combined_text = "\n\n".join(chunk_summaries)
        
        if len(combined_text) > 3000:
            # If combined summaries are still too long, summarize again
            final_prompt = f"""The following are summaries of different sections of a document.
Combine them into a final, comprehensive summary in approximately {max_length} words:

{combined_text}

Final comprehensive summary:"""
        else:
            final_prompt = f"""Combine the following summaries into a final, comprehensive summary in approximately {max_length} words:

{combined_text}

Final summary:"""
        
        final_summary = ask_gemini(final_prompt, temperature=0.3)
        return final_summary
        
    except Exception as e:
        error_msg = f"Error generating summary: {str(e)}"
        print(error_msg)
        return error_msg

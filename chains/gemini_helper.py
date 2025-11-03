"""Helper functions for Google Gemini API integration."""
import google.generativeai as genai
from dotenv import load_dotenv
import os
import config

load_dotenv()

# Configure Gemini API
if config.GEMINI_API_KEY and config.GEMINI_API_KEY != "your_actual_gemini_key_here":
    genai.configure(api_key=config.GEMINI_API_KEY)
    print("🤖 Configured Gemini API")
else:
    print("⚠️  GEMINI_API_KEY not configured")


def list_available_models():
    """List all available Gemini models."""
    try:
        models = genai.list_models()
        available = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                # Remove 'models/' prefix
                name = model.name.replace('models/', '')
                available.append(name)
        return available
    except Exception as e:
        print(f"Error listing models: {str(e)}")
        return []


def normalize_model_name(model: str) -> str:
    """
    Normalize model name to correct format for Gemini API.
    
    Maps common names to actual API model names and handles version updates.
    """
    # Remove 'models/' prefix if present
    model = model.replace('models/', '')
    
    # Model name mappings (updated for current API)
    model_mapping = {
        "gemini-1.5-flash": "gemini-1.5-flash-002",  # Try stable version first
        "gemini-1.5-pro": "gemini-1.5-pro-002",
        "gemini-2.5-flash": "gemini-2.5-flash",
        "gemini-2.5-pro": "gemini-2.5-pro",
        "gemini-pro": "gemini-pro",
        "gemini-flash": "gemini-1.5-flash-002",
    }
    
    # Check if exact match in mapping
    if model in model_mapping:
        return model_mapping[model]
    
    # If already a valid model name (ends with version or is known), return as is
    if any(x in model for x in ['-002', '-latest', '2.5', '1.5-flash-002', '1.5-pro-002']):
        return model
    
    # For gemini-1.5 models, try adding -002 suffix
    if "gemini-1.5" in model and not model.endswith("-002"):
        candidate = f"{model}-002"
        return candidate
    
    # For gemini-2.5 models, return as is
    if "gemini-2.5" in model:
        return model
    
    # Return as is if no mapping found
    return model


def get_best_available_model(preferred: str = None) -> str:
    """
    Get the best available model, trying preferred first, then fallbacks.
    
    Args:
        preferred: Preferred model name
        
    Returns:
        Available model name
    """
    if not preferred:
        preferred = config.LLM_MODEL
    
    available = list_available_models()
    
    if not available:
        return "gemini-pro"  # Ultimate fallback
    
    # Try preferred model
    normalized = normalize_model_name(preferred)
    if normalized in available:
        return normalized
    
    # Try fallback options
    fallbacks = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-preview-05-20",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro-002",
        "gemini-pro"
    ]
    
    for fb in fallbacks:
        if fb in available:
            print(f"⚠️  Using fallback model: {fb}")
            return fb
    
    # Return first available if nothing matches
    return available[0]


def ask_gemini(prompt: str, model: str = None, temperature: float = 0.4) -> str:
    """
    Ask Gemini a question and get a response.
    
    Args:
        prompt: The prompt/question to send to Gemini
        model: Model name (defaults to config.LLM_MODEL)
        temperature: Temperature for generation (0.0-1.0)
        
    Returns:
        Response text from Gemini
    """
    if not model:
        model = config.LLM_MODEL
    
    # Get best available model
    actual_model = get_best_available_model(model)
    
    try:
        # GenerativeModel expects just the model name without 'models/' prefix
        llm = genai.GenerativeModel(actual_model)
        
        response = llm.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            )
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "No response generated from Gemini"
            
    except Exception as e:
        error_msg = str(e)
        
        # If model not found, provide helpful error
        if "not found" in error_msg.lower() or "404" in error_msg:
            print(f"❌ Model '{actual_model}' not found.")
            print("📋 Fetching available models...")
            available = list_available_models()
            if available:
                print("✅ Available models:")
                for m in available[:5]:
                    print(f"   - {m}")
            
            return f"Error: Model not available. Please update LLM_MODEL in .env to one of: {', '.join(available[:3]) if available else 'gemini-pro'}"
        
        error_msg_full = f"Error calling Gemini API: {error_msg}"
        print(error_msg_full)
        return error_msg_full

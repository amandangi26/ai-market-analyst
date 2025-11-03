"""Extraction chain for structured data extraction using Gemini."""
import json
from typing import Dict, Any
from chains.gemini_helper import ask_gemini
import config


def structured_extraction_prompt(text: str, schema: dict, description: str = "Extract structured information") -> str:
    """
    Create a structured extraction prompt with explicit JSON schema.
    
    Args:
        text: Input text to extract from
        schema: Dictionary defining the output schema
        description: Description of what to extract
        
    Returns:
        Formatted prompt string
    """
    schema_description = "\n".join([f'  "{k}": <{v}>' for k, v in schema.items()])
    schema_fields = ', '.join([f'"{k}": <{v}>' for k, v in schema.items()])
    
    prompt = f"""You are an expert data extraction AI. Follow the instructions strictly.

Task: {description}

Input Text:
{text}

Output format (valid JSON only):
{{
{schema_description}
}}

Rules:
- Always output valid JSON only, no explanations.
- Fill missing fields with null.
- Use consistent field names exactly as in schema.
- Do not include extra commentary.
- Validate that output is JSON-parseable.
- Return only the JSON object, nothing else.

Begin extraction:"""
    
    return prompt


def extract_structured_data(text: str, schema: Dict[str, Any], description: str = "Extract structured information") -> Dict[str, Any]:
    """
    Extract structured data from text according to a schema using Gemini.
    
    Args:
        text: Unstructured text to extract from.
        schema: JSON schema defining the structure.
        description: Description of what to extract.
        
    Returns:
        Dictionary containing extracted structured data.
    """
    if not text or len(text.strip()) == 0:
        return {"error": "No text provided for extraction."}
    
    if not schema:
        return {"error": "No schema provided."}
    
    if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "your_actual_gemini_key_here":
        return {"error": "GEMINI_API_KEY not configured"}
    
    try:
        # Create structured prompt
        prompt = structured_extraction_prompt(text, schema, description)
        
        # Get response from Gemini
        result = ask_gemini(prompt, temperature=0.1)
        
        if not result:
            return {"error": "No response from Gemini"}
        
        # Try to parse JSON from result
        result = result.strip()
        
        # Remove markdown code blocks if present
        if result.startswith("```json"):
            result = result[7:]
        elif result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()
        
        # Parse JSON
        try:
            extracted_data = json.loads(result)
            
            # Validate against schema
            if isinstance(extracted_data, dict):
                # Ensure all schema fields are present
                for key in schema.keys():
                    if key not in extracted_data:
                        extracted_data[key] = None
                return extracted_data
            else:
                return {"error": "Extracted data is not a valid object.", "raw": result}
                
        except json.JSONDecodeError as e:
            # Try to find JSON in the response
            try:
                # Look for JSON object in the text
                start = result.find("{")
                end = result.rfind("}") + 1
                if start >= 0 and end > start:
                    json_str = result[start:end]
                    extracted_data = json.loads(json_str)
                    # Ensure all schema fields are present
                    for key in schema.keys():
                        if key not in extracted_data:
                            extracted_data[key] = None
                    return extracted_data
                else:
                    print(f"⚠️  JSON decode error: {str(e)}")
                    print(f"⚠️  Raw response: {result[:500]}")
                    return {"error": f"Could not parse JSON: {str(e)}", "raw": result}
            except Exception as parse_error:
                print(f"⚠️  JSON parse error: {str(parse_error)}")
                print(f"⚠️  Raw response: {result[:500]}")
                return {"error": f"Could not parse JSON: {str(e)}", "raw": result}
        
    except Exception as e:
        error_msg = f"Error during extraction: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

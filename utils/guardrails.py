"""Guardrails for prompt injection detection."""
import re
from fastapi import HTTPException
import config


# Common prompt injection patterns
INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|above)\s+instructions?",
    r"system\s+prompt\s+override",
    r"forget\s+(all|previous|everything)",
    r"you\s+are\s+now\s+(a|an)\s+[^.]*",
    r"act\s+as\s+if\s+you\s+are",
    r"pretend\s+to\s+be",
    r"disregard\s+(the\s+)?(above|previous|instructions)",
    r"new\s+instructions?:",
    r"override\s+(the\s+)?(system|previous|instructions)",
    r"\[INST\]|\[/INST\]",  # Common jailbreak markers
    r"<\|im_start\|>|<\|im_end\|>",  # ChatML markers
]


def check_prompt_injection(text: str) -> bool:
    """
    Check if text contains potential prompt injection patterns.
    
    Args:
        text: Text to check.
        
    Returns:
        True if injection pattern detected, False otherwise.
    """
    if not text:
        return False
    
    text_lower = text.lower()
    
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    
    return False


def validate_input(text: str, input_type: str = "query") -> None:
    """
    Validate input text and raise HTTPException if injection detected.
    
    Args:
        text: Input text to validate.
        input_type: Type of input (query, summary, extract).
        
    Raises:
        HTTPException: If prompt injection is detected and guardrails are enabled.
    """
    if not config.ENABLE_GUARDRAILS:
        return
    
    if not text or len(text.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail=f"{input_type.capitalize()} cannot be empty."
        )
    
    if check_prompt_injection(text):
        raise HTTPException(
            status_code=403,
            detail="Input contains potentially malicious patterns. Request blocked by guardrails."
        )
    
    # Additional validation: length check
    if len(text) > 10000:
        raise HTTPException(
            status_code=400,
            detail=f"{input_type.capitalize()} is too long (max 10000 characters)."
        )


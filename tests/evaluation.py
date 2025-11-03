"""Evaluation utilities for testing chains with Gemini."""
from typing import List, Dict, Any
from chains.qa_chain import answer_question
from chains.summary_chain import summarize_text
from chains.extraction_chain import extract_structured_data


def evaluate_qa_chain(questions: List[str]) -> Dict[str, Any]:
    """
    Evaluate Q&A chain with a list of questions.
    
    Args:
        questions: List of questions to test.
        
    Returns:
        Dictionary with evaluation results.
    """
    results = []
    
    for question in questions:
        try:
            result = answer_question(question)
            results.append({
                "question": question,
                "success": "error" not in result.get("answer", "").lower(),
                "answer_length": len(result.get("answer", "")),
                "has_sources": len(result.get("source_documents", [])) > 0
            })
        except Exception as e:
            results.append({
                "question": question,
                "success": False,
                "error": str(e)
            })
    
    success_rate = sum(1 for r in results if r.get("success", False)) / len(results) if results else 0
    
    return {
        "total_questions": len(questions),
        "success_rate": success_rate,
        "results": results
    }


def evaluate_summary_chain(texts: List[str]) -> Dict[str, Any]:
    """
    Evaluate summary chain with a list of texts.
    
    Args:
        texts: List of texts to summarize.
        
    Returns:
        Dictionary with evaluation results.
    """
    results = []
    
    for text in texts:
        try:
            summary = summarize_text(text)
            results.append({
                "success": "error" not in summary.lower(),
                "original_length": len(text),
                "summary_length": len(summary),
                "compression_ratio": len(summary) / len(text) if text else 0
            })
        except Exception as e:
            results.append({
                "success": False,
                "error": str(e)
            })
    
    success_rate = sum(1 for r in results if r.get("success", False)) / len(results) if results else 0
    
    return {
        "total_texts": len(texts),
        "success_rate": success_rate,
        "results": results
    }


def evaluate_extraction_chain(
    test_cases: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Evaluate extraction chain with test cases.
    
    Args:
        test_cases: List of dicts with 'text' and 'schema' keys.
        
    Returns:
        Dictionary with evaluation results.
    """
    results = []
    
    for case in test_cases:
        try:
            extracted = extract_structured_data(case["text"], case["schema"])
            results.append({
                "success": "error" not in extracted,
                "has_data": bool(extracted and not extracted.get("error"))
            })
        except Exception as e:
            results.append({
                "success": False,
                "error": str(e)
            })
    
    success_rate = sum(1 for r in results if r.get("success", False)) / len(results) if results else 0
    
    return {
        "total_cases": len(test_cases),
        "success_rate": success_rate,
        "results": results
    }


if __name__ == "__main__":
    # Example usage
    print("Evaluation utilities loaded.")
    print("Use these functions to test your chains:")


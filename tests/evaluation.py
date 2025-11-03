"""Evaluation utilities for testing chains with Gemini."""
from typing import List, Dict, Any
from chains.qa_chain import answer_question
from chains.summary_chain import summarize_text
from chains.extraction_chain import extract_structured_data
import time
import math
from typing import Tuple
from ingestion.text_processor import chunk_text

try:
    import google.generativeai as genai
    from google.generativeai.types import content_types
    _HAS_GEMINI = True
except Exception:
    _HAS_GEMINI = False

try:
    import openai
    _HAS_OPENAI = True
except Exception:
    _HAS_OPENAI = False


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


def _cosine(a, b):
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _embed_gemini(texts):
    if not _HAS_GEMINI:
        raise RuntimeError("google-generativeai not available")
    model = "models/text-embedding-004"
    if isinstance(texts, str):
        texts = [texts]
    vectors = []
    for t in texts:
        resp = genai.embed_content(model=model, content=t)
        vectors.append(resp["embedding"])  # type: ignore
    return vectors


def _embed_openai(texts):
    if not _HAS_OPENAI:
        raise RuntimeError("openai package not available")
    if isinstance(texts, str):
        texts = [texts]
    client = openai.OpenAI()  # Requires OPENAI_API_KEY
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in resp.data]


def compare_embedding_models(document_text: str, queries: list[tuple[str, str]]) -> dict:
    """
    Compare Gemini vs OpenAI embeddings on retrieval accuracy & latency.

    Args:
        document_text: Full corpus text to chunk and index
        queries: list of (question, expected_keyword)

    Returns:
        dict report with availability, accuracy and latency per provider
    """
    chunks = chunk_text(document_text, chunk_size=800, chunk_overlap=100)
    report = {"providers": []}

    providers: list[Tuple[str, bool, callable]] = [
        ("Gemini", _HAS_GEMINI, _embed_gemini),
        ("OpenAI", _HAS_OPENAI, _embed_openai),
    ]

    for name, available, embed_fn in providers:
        if not available:
            report["providers"].append({
                "name": name,
                "available": False,
                "reason": "SDK or API key missing"
            })
            continue

        # Precompute chunk embeddings
        t0 = time.time()
        chunk_vecs = embed_fn(chunks)
        index_time_ms = (time.time() - t0) * 1000

        correct = 0
        latencies = []
        for q, expected in queries:
            t1 = time.time()
            qv = embed_fn(q)[0]
            latencies.append((time.time() - t1) * 1000)
            # Retrieve top-1
            sims = [(_cosine(qv, cv), i) for i, cv in enumerate(chunk_vecs)]
            sims.sort(reverse=True)
            top_idx = sims[0][1]
            hit = expected.lower() in chunks[top_idx].lower()
            correct += 1 if hit else 0

        accuracy = (correct / len(queries)) * 100 if queries else 0.0
        avg_latency_ms = sum(latencies) / len(latencies) if latencies else 0.0

        report["providers"].append({
            "name": name,
            "available": True,
            "accuracy_percent": round(accuracy, 2),
            "avg_latency_ms": round(avg_latency_ms, 2),
            "index_time_ms": round(index_time_ms, 2),
            "num_chunks": len(chunks)
        })

    return report


if __name__ == "__main__":
    # Example usage
    print("Evaluation utilities loaded.")
    print("Use these functions to test your chains:")


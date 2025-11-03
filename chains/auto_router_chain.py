"""Autonomous router chain to select the best tool for a user query."""
from typing import Literal
from chains.gemini_helper import ask_gemini


def route_query(user_input: str) -> Literal["qa", "summary", "extract"]:
    """
    Decide which tool to use: qa, summary, or extract.

    Uses a lightweight Gemini model prompt to pick the tool.
    Returns strictly one of: "qa", "summary", "extract".
    """
    instruction = (
        "You are a router that decides which tool best answers a user query.\n"
        "Tools:\n- qa: answer questions using retrieval over documents\n"
        "- summary: summarize or condense provided text\n"
        "- extract: extract structured fields or JSON from text based on a schema\n\n"
        "Given the user query, respond with only one word: qa, summary, or extract.\n"
        "No punctuation, no extra words."
    )

    prompt = f"""
{instruction}

User query:
{user_input}

Answer (one word):
""".strip()

    # Prefer a fast model; gemini_helper will normalize and fallback as needed
    response = ask_gemini(prompt, model="gemini-1.5-flash", temperature=0.0)
    answer = (response or "").strip().lower()

    if "extract" in answer:
        return "extract"
    if "summary" in answer or "summarize" in answer:
        return "summary"
    return "qa"



"""API routes for AI Market Analyst."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import utils.guardrails as guardrails
from chains.qa_chain import answer_question
from chains.summary_chain import summarize_text
from chains.extraction_chain import extract_structured_data

router = APIRouter()


# Request/Response models
class QARequest(BaseModel):
    question: str = Field(..., description="Question to answer")


class QAResponse(BaseModel):
    answer: str
    source_documents: list


class SummaryRequest(BaseModel):
    text: str = Field(..., description="Text to summarize")
    max_length: Optional[int] = Field(500, description="Maximum summary length in words")


class SummaryResponse(BaseModel):
    summary: str


class ExtractRequest(BaseModel):
    text: str = Field(..., description="Text to extract from")
    json_schema: Dict[str, Any] = Field(..., alias="schema", description="JSON schema for extraction")
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class ExtractResponse(BaseModel):
    data: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    message: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "AI Market Analyst API is running"
    }


@router.post("/qa", response_model=QAResponse)
async def qa_endpoint(request: QARequest):
    """Answer questions using RAG pipeline."""
    try:
        guardrails.validate_input(request.question, "query")
        result = answer_question(request.question)
        return QAResponse(
            answer=result["answer"],
            source_documents=result.get("source_documents", [])
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@router.post("/summary", response_model=SummaryResponse)
async def summary_endpoint(request: SummaryRequest):
    """Summarize long text."""
    try:
        guardrails.validate_input(request.text, "summary")
        summary = summarize_text(request.text, request.max_length or 500)
        return SummaryResponse(summary=summary)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@router.post("/extract", response_model=ExtractResponse)
async def extract_endpoint(request: ExtractRequest):
    """Extract structured data from unstructured text."""
    try:
        guardrails.validate_input(request.text, "extract")
        if not request.json_schema:
            raise HTTPException(status_code=400, detail="Schema is required")
        
        extracted = extract_structured_data(request.text, request.json_schema, description="Extract structured data from the text")
        
        if "error" in extracted:
            raise HTTPException(status_code=500, detail=extracted["error"])
        
        return ExtractResponse(data=extracted)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during extraction: {str(e)}")


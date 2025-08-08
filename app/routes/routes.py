# app/routes/routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from app.services.document_parser import parse_document
from app.services.chunker import chunk_text
from app.services.semantic_search import get_similar_chunks
from app.services.clause_matcher import match_clauses
from app.services.response_builder import build_json_response
import logging

router = APIRouter()

class HackRxRequest(BaseModel):
    documents: list[str]
    questions: list[str]

    @validator('documents')
    def non_empty_docs(cls, v):
        if not v or all(not d.strip() for d in v):
            raise ValueError('At least one non-empty document is required')
        return v

    @validator('questions')
    def non_empty_questions(cls, v):
        if not v or all(not q.strip() for q in v):
            raise ValueError('At least one non-empty question is required')
        return v

@router.post("/hackrx/run")
def run_hackrx_submission(request: HackRxRequest):
    try:
        combined_text = "\n".join(request.documents)
        chunks = chunk_text(combined_text)
        similar_chunks = get_similar_chunks(chunks, request.questions)
        answers = match_clauses(similar_chunks, request.questions)
        return build_json_response(answers)
    except Exception as e:
        logging.error(f"Error in /hackrx/run: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

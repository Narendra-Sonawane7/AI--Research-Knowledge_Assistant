from pydantic import BaseModel, Field
from typing import List, Optional


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)


class QARequest(BaseModel):
    question: str = Field(..., min_length=1)
    document_id: Optional[int] = None


class CompareRequest(BaseModel):
    document_ids: List[int] = Field(..., min_length=2)
    topic: str = "comparison"


class SummaryRequest(BaseModel):
    document_id: int
    style: str = "executive"


class ClassifyRequest(BaseModel):
    document_id: int


class QAResponse(BaseModel):
    answer: str
    sources: List[str] = []
    pages: List[int] = []
    retrieved_context: List[str] = []
    confidence: float = 0.0

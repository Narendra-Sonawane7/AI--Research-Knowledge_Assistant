from fastapi import APIRouter
from app.schemas import SummaryRequest
from app.services.summary_service import summarize_document

router = APIRouter(prefix="/summary", tags=["Summary"])


@router.post("")
def summary(req: SummaryRequest):
    return {"document_id": req.document_id, "summary": summarize_document(req.document_id, req.style)}

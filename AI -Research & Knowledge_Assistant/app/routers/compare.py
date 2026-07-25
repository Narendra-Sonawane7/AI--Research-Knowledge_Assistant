from fastapi import APIRouter
from app.schemas import CompareRequest
from app.services.compare_service import compare_documents

router = APIRouter(prefix="/compare", tags=["Compare"])


@router.post("")
def compare(req: CompareRequest):
    return {"topic": req.topic, "comparison": compare_documents(req.document_ids, req.topic)}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.document import Document

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("")
def analytics(db: Session = Depends(get_db)):
    total_documents = db.query(func.count(Document.id)).scalar() or 0
    total_chunks = db.query(func.sum(Document.total_chunks)).scalar() or 0
    processed = db.query(func.count(Document.id)).filter(Document.status == "processed").scalar() or 0

    return {
        "total_documents": total_documents,
        "total_chunks": total_chunks,
        "processed_documents": processed,
    }

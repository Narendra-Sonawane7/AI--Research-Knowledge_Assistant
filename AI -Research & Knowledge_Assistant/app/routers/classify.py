from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document
from app.services.classification_service import classify_text

router = APIRouter(prefix="/classify", tags=["Classify"])


@router.post("")
def classify(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        return {"error": "Document not found"}

    with open(doc.stored_path, "rb") as f:
        raw = f.read()

    text = raw.decode("latin-1", errors="ignore")
    result = classify_text(text[:3000])

    doc.category = result["category"]
    db.commit()

    return {"document_id": doc.id, **result}

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
import shutil
import os

from app.config import settings
from app.database import get_db
from app.models.document import Document
from app.services.pdf_service import extract_pages_and_chunks
from app.services.vector_store import VectorStore
from app.services.classification_service import classify_text
from app.services.groq_service import ask_groq

router = APIRouter(prefix="/documents", tags=["Documents"])
vector_store = VectorStore()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    saved_path = upload_dir / f"{datetime.utcnow().timestamp()}_{file.filename}"
    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    total_pages, pages_data, chunks = extract_pages_and_chunks(str(saved_path))
    full_text = " ".join([p["text"] for p in pages_data]).strip()

    doc = Document(
        filename=file.filename,
        stored_path=str(saved_path),
        upload_time=datetime.utcnow(),
        total_pages=total_pages,
        total_chunks=len(chunks),
        status="processed",
        category=classify_text(full_text[:3000])["category"] if full_text else "Unknown",
        summary="",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    vector_store.add_chunks(doc.id, file.filename, chunks)

    if full_text:
        doc.summary = ask_groq(
            system_prompt="Summarize the document in 4-5 lines.",
            user_prompt=full_text[:12000],
        )
        db.commit()

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "total_pages": doc.total_pages,
        "total_chunks": doc.total_chunks,
        "category": doc.category,
    }


@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.upload_time.desc()).all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "upload_time": d.upload_time,
            "total_pages": d.total_pages,
            "total_chunks": d.total_chunks,
            "status": d.status,
            "category": d.category,
        }
        for d in docs
    ]


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    vector_store.delete_document(document_id)
    if os.path.exists(doc.stored_path):
        os.remove(doc.stored_path)

    db.delete(doc)
    db.commit()
    return {"message": "Document deleted"}

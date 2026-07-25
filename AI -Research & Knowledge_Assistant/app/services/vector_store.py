from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from app.config import settings


class VectorStore:
    def __init__(self):
        self.client = PersistentClient(path=settings.CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(name="doc_chunks")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_chunks(self, document_id: int, filename: str, chunks: list[dict]):
        texts = [c["text"] for c in chunks]
        if not texts:
            return
        ids = [f"{document_id}_{i}" for i in range(len(chunks))]
        embeddings = self.model.encode(texts).tolist()
        metadatas = [
            {"document_id": document_id, "filename": filename, "page": c["page"], "text": c["text"]}
            for c in chunks
        ]
        self.collection.add(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)

    def search(self, query: str, document_id: int | None = None, top_k: int = 5):
        q_emb = self.model.encode([query]).tolist()[0]
        where = {"document_id": document_id} if document_id is not None else None
        return self.collection.query(query_embeddings=[q_emb], n_results=top_k, where=where)

    def delete_document(self, document_id: int):
        try:
            result = self.collection.get(where={"document_id": document_id})
            ids = result.get("ids", [])
            if ids:
                self.collection.delete(ids=ids)
        except Exception:
            pass

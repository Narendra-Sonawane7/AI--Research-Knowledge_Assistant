from app.services.vector_store import VectorStore
from app.services.groq_service import ask_groq

vector_store = VectorStore()


def build_context(search_result: dict):
    documents = search_result.get("documents", [[]])[0]
    metadatas = search_result.get("metadatas", [[]])[0]

    context_items = []
    sources = []
    pages = []

    for doc, meta in zip(documents, metadatas):
        context_items.append(f"[Page {meta.get('page')}] {doc}")
        sources.append(meta.get("filename", "unknown"))
        pages.append(meta.get("page", 0))

    return context_items, sources, pages


def answer_question(question: str, document_id: int | None = None):
    search_result = vector_store.search(question, document_id=document_id, top_k=5)
    context_items, sources, pages = build_context(search_result)

    if not context_items:
        return {
            "answer": "I could not find relevant information in the uploaded documents.",
            "sources": [],
            "pages": [],
            "retrieved_context": [],
            "confidence": 0.0,
        }

    context_text = "\n\n".join(context_items)

    prompt = f"""
You are a helpful assistant.
Answer only from the provided context.
If the context is not enough, say you cannot determine the answer.

Question:
{question}

Context:
{context_text}

Return a short, clear answer.
"""

    answer = ask_groq(
        system_prompt="You answer only from the provided document context.",
        user_prompt=prompt,
    )

    return {
        "answer": answer,
        "sources": list(dict.fromkeys(sources)),
        "pages": sorted(list(set(pages))),
        "retrieved_context": context_items,
        "confidence": 0.85 if "could not" not in answer.lower() else 0.0,
    }

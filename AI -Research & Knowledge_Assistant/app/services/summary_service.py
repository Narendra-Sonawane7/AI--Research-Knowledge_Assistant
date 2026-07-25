from app.services.vector_store import VectorStore
from app.services.groq_service import ask_groq

vector_store = VectorStore()


def summarize_document(document_id: int, style: str = "executive"):
    search_result = vector_store.search("summary", document_id=document_id, top_k=8)
    docs = search_result.get("documents", [[]])[0]
    metas = search_result.get("metadatas", [[]])[0]

    context = []
    for d, m in zip(docs, metas):
        context.append(f"[Page {m.get('page')}] {d}")

    context_text = "\n\n".join(context)

    prompt = f"""
Create a {style} summary of this document content.

Content:
{context_text}

Return:
- Executive Summary
- Technical Summary
- Bullet Point Summary
- Key Takeaways
"""

    return ask_groq(
        system_prompt="You summarize only the given document content.",
        user_prompt=prompt,
    )

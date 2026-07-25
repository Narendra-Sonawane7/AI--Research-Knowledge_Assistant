from app.services.vector_store import VectorStore
from app.services.groq_service import ask_groq

vector_store = VectorStore()


def compare_documents(document_ids: list[int], topic: str):
    blocks = []
    for doc_id in document_ids:
        search_result = vector_store.search(topic, document_id=doc_id, top_k=5)
        docs = search_result.get("documents", [[]])[0]
        metas = search_result.get("metadatas", [[]])[0]
        joined = "\n".join([f"[Page {m.get('page')}] {d}" for d, m in zip(docs, metas)])
        blocks.append(f"Document {doc_id}:\n{joined}")

    prompt = f"""
Compare the following documents on topic: {topic}

{chr(10).join(blocks)}

Return similarities, differences, pros/cons, and conclusion.
"""

    return ask_groq(
        system_prompt="You compare documents only from the given content.",
        user_prompt=prompt,
    )

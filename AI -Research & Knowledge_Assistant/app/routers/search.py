from fastapi import APIRouter

from app.schemas import SearchRequest
from app.services.vector_store import VectorStore
from app.services.hybrid_search import HybridSearch
from app.services.reranker import Reranker

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

vector_store = VectorStore()
reranker = Reranker()


@router.post("")
def semantic_search(req: SearchRequest):

    result = vector_store.search(
        req.query,
        top_k=5
    )

    if isinstance(result, dict):

        documents = result.get(
            "documents",
            [[]]
        )[0]

    else:
        documents = result

    hybrid_results = HybridSearch.search(
        req.query,
        documents
    )

    final_results = reranker.rerank(
        req.query,
        hybrid_results
    )

    return {
        "query": req.query,
        "results": final_results[:3]
    }
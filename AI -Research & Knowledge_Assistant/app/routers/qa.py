from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas import QARequest
from app.services.rag_service import answer_question
from app.services.streaming_service import StreamingService
from app.services.cache_service import CacheService
from app.services.groq_service import ask_groq

router = APIRouter(
    prefix="/qa",
    tags=["Q&A"]
)

cache = CacheService()


@router.post("")
def qa(req: QARequest):

    # Check Redis Cache
    cached = cache.get(
        req.question
    )

    if cached:

        return {
            "answer": cached,
            "source": "cache"
        }

    # Existing RAG Pipeline
    response = answer_question(
        req.question,
        document_id=req.document_id
    )

    # Save to Cache
    cache.set(
        req.question,
        response
    )

    return {
        "answer": response,
        "source": "groq"
    }


@router.post("/stream")
async def stream_answer(
        req: QARequest
):

    # Check Cache
    cached = cache.get(
        req.question
    )

    if cached:

        return StreamingResponse(
            StreamingService.stream_text(
                cached
            ),
            media_type="text/plain"
        )

    # Call Groq
    answer = ask_groq(
        "You are a helpful AI assistant.",
        req.question
    )

    # Save in Redis
    cache.set(
        req.question,
        answer
    )

    return StreamingResponse(
        StreamingService.stream_text(
            answer
        ),
        media_type="text/plain"
    )
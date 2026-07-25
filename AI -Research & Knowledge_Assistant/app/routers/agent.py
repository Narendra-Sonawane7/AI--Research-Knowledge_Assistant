from fastapi import APIRouter

from app.agents.graph import (
    run_agent
)

router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)


@router.post("")
def agent(
        query: str
):

    response = run_agent(
        query
    )

    return {
        "query": query,
        "response": response
    }
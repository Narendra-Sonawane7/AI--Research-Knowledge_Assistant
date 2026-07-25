from typing import TypedDict

from app.agents.tools import (
    qa_tool,
    summary_tool
)


class AgentState(
        TypedDict
):

    query: str
    response: str


def run_agent(
        query
):

    if "summarize" in query.lower():

        result = summary_tool(
            query
        )

    else:

        result = qa_tool(
            query
        )

    return result
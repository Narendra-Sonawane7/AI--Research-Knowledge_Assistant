from app.services.rag_service import answer_question
from app.services.summary_service import summarize_document
from app.services.comparison_service import compare_documents


def qa_tool(question):

    return answer_question(
        question
    )


def summary_tool(text):

    return summarize_document(
        text
    )


def compare_tool(
        doc1,
        doc2
):

    return compare_documents(
        doc1,
        doc2
    )
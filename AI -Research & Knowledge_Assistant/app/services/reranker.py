from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
            self,
            query,
            documents
    ):

        if not documents:
            return []

        pairs = [
            [query, doc["text"]]
            for doc in documents
        ]

        scores = self.model.predict(
            pairs
        )

        results = []

        for doc, score in zip(
                documents,
                scores
        ):

            doc["rerank_score"] = float(
                score
            )

            results.append(
                doc
            )

        results.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return results
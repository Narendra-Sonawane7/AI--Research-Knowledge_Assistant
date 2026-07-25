from rank_bm25 import BM25Okapi


class HybridSearch:

    @staticmethod
    def search(query, documents):

        tokenized_docs = [
            doc.split()
            for doc in documents
        ]

        bm25 = BM25Okapi(
            tokenized_docs
        )

        scores = bm25.get_scores(
            query.split()
        )

        results = []

        for doc, score in zip(
                documents,
                scores
        ):

            results.append(
                {
                    "text": doc,
                    "bm25_score": float(score)
                }
            )

        results.sort(
            key=lambda x: x["bm25_score"],
            reverse=True
        )

        return results

def compare_documents(
        text1,
        text2
):

    similarities = []

    words1 = set(
        text1.lower().split()
    )

    words2 = set(
        text2.lower().split()
    )

    common = words1.intersection(
        words2
    )

    return {
        "common_words": list(common),
        "similarity_score":
        len(common) /
        max(
            len(words1),
            len(words2)
        )
    }
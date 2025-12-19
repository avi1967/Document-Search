from sentence_transformers import CrossEncoder

# Correct model for reranking
reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, chunks, top_k=3):
    if not chunks:
        return []

    pairs = [(query, c["content"]) for c in chunks]

    scores = reranker_model.predict(pairs)

    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [c for c, _ in ranked[:top_k]]

from ingestion.embedder import embed_text
from retrieval.reranker import rerank

def retrieve(query, vector_store, k=5):
    query_embedding = embed_text([query])[0]
    results = vector_store.search(query_embedding, k=k)

    print("RETRIEVE RESULTS:", len(results))
    if results:
        print("FIRST RESULT PREVIEW:", results[0]["content"][:200])
    # Rerank for quality
    reranked = rerank(query, results)
    return reranked

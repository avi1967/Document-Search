from sentence_transformers import SentenceTransformer

# Lightweight local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(texts):
    """
    Generate embeddings locally using sentence-transformers
    """
    embeddings = model.encode(texts)
    return embeddings.tolist()

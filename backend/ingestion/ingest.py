from ingestion.loader import load_pdf
from ingestion.embedder import embed_text
from ingestion.chunker import chunk_pages

def ingest_pdf(file_path, vector_store):
    pages = load_pdf(file_path)
    if not pages:
        return 0

    chunks = chunk_pages(pages, chunk_size=300, overlap=50)
    if not chunks:
        return 0

    print("INGESTION DEBUG")
    print("Total chunks:", len(chunks))
    print("First chunk:", chunks[0]["content"][:150])

    texts = [c["content"] for c in chunks]
    embeddings = embed_text(texts)

    vector_store.add(embeddings, chunks)

    return len(chunks)

from ingestion.loader import load_pdf
from ingestion.embedder import embed_text

CHUNK_SIZE = 200  # smaller = better retrieval

def chunk_text(text, document):
    chunks = []
    paragraphs = text.split("\n\n")

    for para in paragraphs:
        para = para.strip()
        if len(para) < 50:
            continue

        for i in range(0, len(para), CHUNK_SIZE):
            chunk = para[i:i + CHUNK_SIZE]

            chunks.append({
                "content": chunk,
                "document": document,
                "page": None
            })

    return chunks


def ingest_pdf(file_path, vector_store):
    pages = load_pdf(file_path)

    full_text = "\n".join([p["content"] for p in pages])
    document = pages[0]["document"]

    chunks = chunk_text(full_text, document)

    print("INGESTION DEBUG")
    print("Total chunks:", len(chunks))
    print("First chunk:", chunks[0]["content"][:150])

    texts = [c["content"] for c in chunks]
    embeddings = embed_text(texts)

    vector_store.add(embeddings, chunks)

    return len(chunks)

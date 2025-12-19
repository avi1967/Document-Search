def chunk_pages(pages, chunk_size=500, overlap=50):
    chunks = []

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "content": chunk_text,
                "page": page["page"]
            })

            start = end - overlap

    return chunks

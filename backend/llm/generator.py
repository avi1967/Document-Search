import ollama

def generate_answer(context, question):
    prompt = f"""
You are a document analysis assistant.

Instructions:
- Answer using ONLY the provided context
- You may summarize or paraphrase
- Do NOT add information not present in the context
- If the context is empty, say "No relevant content found in the document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"].strip()

def build_prompt(context, question):
    return f"""
You are an assistant. Answer ONLY using the context.

Context:
{context}

Question:
{question}
"""

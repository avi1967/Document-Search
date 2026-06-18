from config import settings
import ollama
import requests

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

    if settings.USE_OPENAI and settings.OPENAI_API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": settings.LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0
            }
            res = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"OpenAI Generation Error: {str(e)}. Please check your API key or network connection."

    # Default to Ollama local generation
    model_name = settings.LLM_MODEL if not settings.LLM_MODEL.startswith("gpt-") else "llama3"
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"].strip()
    except Exception as e:
        # Format the context nicely for the fallback answer
        formatted_context = context.strip() if context else "No relevant context was found in the document."
        return (
            f"⚠️ **LLM Offline Fallback Mode**\n\n"
            f"Could not connect to the local Ollama model '{model_name}' or OpenAI API.\n"
            f"However, here is the most relevant section found in the document:\n\n"
            f"\"\"\"\n"
            f"{formatted_context}\n"
            f"\"\"\"\n\n"
            f"*To enable AI synthesis, start Ollama locally (http://127.0.0.1:11434) or configure your API keys in config.py.*"
        )

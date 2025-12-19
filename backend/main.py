from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from models.schemas import QueryRequest
from ingestion.ingest import ingest_pdf
from retrieval.vector_store import VectorStore
from retrieval.retriever import retrieve
from llm.generator import generate_answer

from fastapi.responses import FileResponse

app = FastAPI()

# CORS (for React later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure folders exist
os.makedirs("data/raw_docs", exist_ok=True)
os.makedirs("data/vector_index", exist_ok=True)

# Initialize vector store
vector_store = VectorStore(dim=384)

@app.get("/")
def root():
    return {
        "message": "LLM Document Query System is running 🚀",
        "docs": "/docs"
    }

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    file_path = f"data/raw_docs/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = ingest_pdf(file_path, vector_store)

    return {
        "status": "success",
        "chunks_ingested": chunks,
        "file": file.filename
    }

@app.post("/query")

@app.post("/query")
def query_docs(request: QueryRequest):
    question = request.question

    results = retrieve(question, vector_store)

    if not results:
        return {
            "answer": "No relevant content found in the document.",
            "citations": []
        }

    context = "\n".join([r["content"] for r in results])
    answer = generate_answer(context, question)

    citations = [
        {"document": r["document"], "page": r["page"]}
        for r in results
    ]

    return {
        "answer": answer,
        "citations": citations
    }


@app.get("/pdf/{filename}")
def get_pdf(filename: str):
    path = f"data/raw_docs/{filename}"
    return FileResponse(path, media_type="application/pdf")

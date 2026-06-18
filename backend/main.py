from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from config import settings
from models.schemas import QueryRequest
from ingestion.ingest import ingest_pdf
from retrieval.vector_store import VectorStore
from retrieval.retriever import retrieve
from llm.generator import generate_answer

from fastapi.responses import FileResponse

app = FastAPI()

# CORS (for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development flexibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure folders exist
os.makedirs(settings.RAW_DOCS_PATH, exist_ok=True)
os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)

# Initialize vector store
vector_store = VectorStore(dim=settings.VECTOR_DIM, path=settings.VECTOR_DB_PATH)

@app.get("/")
def root():
    return {
        "message": "LLM Document Query System is running 🚀",
        "docs": "/docs"
    }

@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(settings.RAW_DOCS_PATH, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = ingest_pdf(file_path, vector_store)

    return {
        "status": "success",
        "chunks_ingested": chunks,
        "file": file.filename
    }

@app.post("/query")
def query_docs(request: QueryRequest):
    question = request.question

    results = retrieve(question, vector_store, k=request.top_k or settings.TOP_K)

    if not results:
        return {
            "answer": "No relevant content found in the document.",
            "citations": []
        }

    context = "\n".join([r["content"] for r in results])
    answer = generate_answer(context, question)

    # Deduplicate citations to keep the UI clean
    citations = []
    seen = set()
    for r in results:
        doc = r.get("document")
        page = r.get("page")
        if doc and page:
            key = (doc, page)
            if key not in seen:
                seen.add(key)
                citations.append({"document": doc, "page": page})

    return {
        "answer": answer,
        "citations": citations
    }

@app.get("/pdf/{filename}")
def get_pdf(filename: str):
    path = os.path.join(settings.RAW_DOCS_PATH, filename)
    return FileResponse(path, media_type="application/pdf")

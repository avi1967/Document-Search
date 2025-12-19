# 📄 LLM-Powered Intelligent Document Search System

An LLM-powered Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents and ask natural language questions.
The system retrieves relevant content from the document and generates grounded answers with citations, running fully locally without cloud APIs.

## 🚀 Features

📂 Upload PDF documents

🔍 Semantic search using embeddings

🤖 Natural language question answering

📑 Document-grounded responses (no hallucinations)

📌 Source citations (document & page)

🧠 Local LLM inference (no OpenAI dependency)

🖥️ Web-based UI built with React

⚡ FastAPI backend

## 🏗️ System Architecture
User (Browser)
     |
     v
React Frontend
     |
     v
FastAPI Backend
     |
     ├── PDF Loader & Chunker
     ├── Sentence Embeddings (Sentence Transformers)
     ├── Vector Store (local storage)
     ├── Retriever + Reranker
     └── LLM (Ollama / LLaMA)

## 🧰 Tech Stack
Backend

Python

FastAPI

Sentence Transformers

Ollama (LLaMA 3)

PyPDF2

NumPy

Frontend

React

JavaScript

HTML / CSS


## 🧪 How to Use

1. Start backend and frontend

2. Upload a PDF document

3. Ask questions such as:

“What is this document about?”

“What is the termination notice period?”

4. View answers with cited sources

5. Click citations to inspect document context

✅ Example Output

Question:

What is the termination notice period?

Answer:

Contractors may be terminated with 30 days written notice as stated in the policy.

Sources:

sample_policy.pdf (page 1)

## 🔒 Privacy & Security

- Runs completely offline

- No data is sent to third-party APIs

- Uploaded documents remain local

## 🚧 Limitations

- Works best with text-based PDFs

- OCR is not enabled for scanned documents

- Vector storage is local (not distributed)

## 🔮 Future Improvements

- Dockerized backend and frontend

- OCR support for scanned PDFs

- Highlighted citations in PDF preview

- Chat history / conversational memory

- Advanced UI enhancements

## 🎓 Academic Use

This project demonstrates:

1. Retrieval-Augmented Generation (RAG)

2. Semantic search

3. LLM grounding

4. Full-stack ML system design


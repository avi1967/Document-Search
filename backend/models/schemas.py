from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5


class SourceChunk(BaseModel):
    content: str
    document_name: Optional[str]
    page_number: Optional[int]


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    confidence: Optional[float] = None


class IngestResponse(BaseModel):
    status: str
    documents_ingested: int

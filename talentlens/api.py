from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from talentlens.extraction import extract_structured_resume
from talentlens.llm import OllamaUnavailableError
from talentlens.parsing import parse_resume_file
from talentlens.rag.answer import answer_with_citations
from talentlens.rag.logging import log_retrieval
from talentlens.rag.retrieval import ResumeRetriever
from talentlens.rag.index import ResumeIndex
from talentlens.storage import ensure_data_dirs, load_resume, save_processed_resume, save_raw_resume


app = FastAPI(title="TalentLens AI", version="0.1.0")
RESUME_ID_PATTERN = r"^[A-Za-z0-9_-]+$"


class ChatRequest(BaseModel):
    resume_id: str = Field(
        ...,
        min_length=1,
        pattern=RESUME_ID_PATTERN,
        description="Resume ID returned from upload.",
    )
    question: str
    top_k: int = 4


class ChatResponse(BaseModel):
    answer: str
    citations: list[str]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)) -> dict[str, str | int]:
    ensure_data_dirs()
    resume_id = f"res_upload_{uuid.uuid4().hex[:8]}"
    content = await file.read()
    filename = file.filename or f"{resume_id}.txt"
    raw_path = save_raw_resume(resume_id, filename, content)
    resume_text = parse_resume_file(Path(raw_path))
    try:
        structured = extract_structured_resume(resume_text)
    except OllamaUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                f"Ollama is not reachable: {str(exc)}. Start Ollama and verify OLLAMA_BASE_URL "
                "before calling /upload_resume."
            ),
        ) from exc
    save_processed_resume(resume_id, resume_text, structured, Path(raw_path))
    indexer = ResumeIndex()
    chunk_count = indexer.index_resume(resume_id, resume_text)
    return {"resume_id": resume_id, "chunks_indexed": chunk_count}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        resume_record = load_resume(request.resume_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Resume '{request.resume_id}' not found. "
                "Upload a resume first and use the returned resume_id."
            ),
        ) from exc
    retriever = ResumeRetriever()
    chunks = retriever.retrieve(
        request.question, top_k=request.top_k, resume_id=resume_record["id"]
    )
    log_retrieval(request.question, chunks)
    payload = answer_with_citations(request.question, chunks)
    return ChatResponse(answer=payload["answer"], citations=payload["citations"])

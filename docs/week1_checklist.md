Week 1 Checklist — Foundation

Goal: Build a resume-only RAG foundation, ingest initial data, and start the golden eval set.

1) Corpus finalization (resumes + 10 JDs + policies)
- [ ] Download resume datasets (Kaggle: Livecareer Resume Dataset, Resume Dataset)
- [ ] Download JD datasets (Kaggle: LinkedIn Job Postings 2023, Job Description Dataset)
- [ ] Choose a role family (e.g., Data/ML) and filter datasets to that scope
- [ ] Collect hiring policies (GitLab Handbook Interview Guides)
- [ ] Store raw files with consistent IDs and metadata

2) Resume upload + structured parsing (LLM JSON extraction)
- [ ] Implement PDF/DOCX upload endpoint (FastAPI)
- [ ] Parse resume text (pypdf/pdfplumber)
- [ ] Extract structured JSON via LLM (name, experience, skills, roles, education, projects)
- [ ] Persist extracted JSON next to raw resume

3) Resume-only RAG (single corpus)
- [ ] Section-aware chunking (per role/project/education section)
- [ ] Generate embeddings for chunks
- [ ] Store vectors in ChromaDB with metadata
- [ ] Implement retrieval + answer generation with citations
- [ ] Log retrieved chunks for each query (debugging)

4) Golden eval set — first 30 cases
- [ ] Create eval file (golden_eval.json)
- [ ] Add 30 Type A factual retrieval cases
- [ ] Each case includes: id, resume_id, question, reference_answer, expected_source_span, difficulty

Minimum demo for Week 1 checkpoint
- Upload a resume
- Ask 3 factual questions
- Show citations in every answer

Notes
- Hand-rolled RAG only (no LangChain/LlamaIndex)
- Citations required in every response
- Keep data scope tight for higher eval quality

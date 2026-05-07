Week 2 Checklist — Multi-source RAG

Goal: Index all corpora, add query routing, complete golden eval set.

1) Multi-source indexing
- [ ] Index Resume corpus with per-source metadata
- [ ] Index JD Library corpus with per-source metadata
- [ ] Index Hiring Policies corpus with per-source metadata
- [ ] Store in ChromaDB with source tags (resume/jd/policy)

2) Query router
- [ ] Implement query classifier/router to select corpus
- [ ] Support multi-corpus queries when needed
- [ ] Log routing decision for each query

3) Match scorer v1
- [ ] Implement initial match scoring (embedding cosine + heuristics)
- [ ] Return score + rationale (even if simple)

4) Golden eval set complete (100 cases)
- [ ] 50 factual retrieval cases (Type A)
- [ ] 30 match quality cases (Type B)
- [ ] 20 interview quality cases (Type C)
- [ ] Ensure diversity in topics, difficulty, and roles

5) Baseline eval run
- [ ] Compute recall@k and MRR for retrieval
- [ ] Store baseline metrics for comparison

Minimum demo for Week 2 checkpoint
- Ask questions that hit all 3 corpora
- Show routing decisions and citations
- Show match scorer output
- Present completed 100-case eval set

Notes
- Keep role family focused
- Ensure eval set is hand-written (no LLM generation)
- Do not add reranker yet; establish baseline first

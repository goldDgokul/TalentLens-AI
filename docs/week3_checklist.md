Week 3 Checklist — Intelligence Layer

Goal: Add hybrid retrieval, reranking, conversational follow-ups, interview generation, and LLM-judge evaluation.

1) Hybrid retrieval + reranker
- [ ] Add BM25 retrieval alongside dense embeddings
- [ ] Fuse results (BM25 + dense)
- [ ] Add cross-encoder reranker (BAAI/bge-reranker-base)
- [ ] Log retrieval + rerank diagnostics

2) Match rationale with citations
- [ ] Generate match rationale grounded in resume + JD
- [ ] Ensure citations for each rationale point

3) Conversational follow-ups
- [ ] Implement query rewriting using conversation history
- [ ] Test on ≥10 follow-up scenarios with pronouns/ellipsis
- [ ] Document comparison: history-in-prompt vs query-rewriting

4) Interview question generator
- [ ] Generate 8–12 questions per resume–JD pair
- [ ] Tag each by topic, difficulty, rationale
- [ ] Ground questions in hiring rubric

5) LLM-as-judge pipeline
- [ ] Implement judge scoring for response quality
- [ ] Validate against ≥20 human-scored samples
- [ ] Report agreement (Cohen’s kappa or Spearman)

Minimum demo for Week 3 checkpoint
- Multi-turn conversation with follow-ups
- Show hybrid retrieval + reranker effect
- Show interview question output + citations
- Present judge-vs-human agreement metrics

Notes
- Keep eval reproducible (one-command run)
- Log retrieval misses and categorize errors

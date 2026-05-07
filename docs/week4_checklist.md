Week 4 Checklist — Production Polish

Goal: Observability, bias guardrails, failure analysis, deployment, and final report.

1) Observability
- [ ] Track cost per query (tokens + model)
- [ ] Track latency per endpoint
- [ ] Store logs in CSV/JSON for analysis

2) Bias & fairness guardrails (stretch)
- [ ] Detect/flag protected-attribute queries
- [ ] Refuse unsafe requests with policy message
- [ ] Log flagged queries for audit
- [ ] Document policy in model card

3) Failure analysis
- [ ] Identify top 20 worst cases
- [ ] Categorize by failure type (retrieval, generation, routing, parsing)
- [ ] Propose mitigations for each

4) Deployment
- [ ] Deploy FastAPI service (Render/Railway/Fly.io)
- [ ] Verify public URL + endpoints
- [ ] Document deployment steps

5) Final artifacts
- [ ] Final report (5–8 pages)
- [ ] Model card with intended use, risks, fairness
- [ ] Demo video (5–7 minutes)

Minimum demo for Week 4 checkpoint
- Live walkthrough on deployed URL
- Show observability logs
- Present failure analysis and mitigation plan

Notes
- Ensure citations in every response
- Include real regulation references (NYC Local Law 144, EU AI Act)

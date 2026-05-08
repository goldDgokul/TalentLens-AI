# TalentLens-AI
An Intelligent Recruitment Co-pilot Powered by Retrieval-Augmented Generation and Generative AI.

## Week 1 Setup (Resume-only RAG)

### 1) Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure Kaggle datasets
1. Add Kaggle API credentials:
   - Export `KAGGLE_USERNAME` and `KAGGLE_KEY`, or
   - Place `~/.kaggle/kaggle.json`.
2. Fill in `data/kaggle_datasets.json` with the correct Kaggle dataset slugs.

### 3) Download and normalize datasets
```bash
python -m talentlens.data.kaggle
python -m talentlens.data.normalize
python -m talentlens.data.policies
```

### 4) Build the resume-only index
```bash
python -m talentlens.rag.index
```

### 5) Run the API
```bash
uvicorn main:app --reload
```

### Environment variables
- `OPENAI_API_KEY` (optional): only needed when `LLM_PROVIDER=openai` and you want OpenAI-backed extraction/answers.
- `LLM_PROVIDER` (optional, default: `openai`): supports `openai`, `mock`, and `none`.
  - If `LLM_PROVIDER=openai` but `OPENAI_API_KEY` is not set, the app gracefully falls back to heuristic extraction/answers.
- `EMBEDDING_BACKEND` (optional, default: `sentence-transformers`): set to `hash` for lightweight local/demo runs.

### 6) Demo (sample resume)
Use the provided sample resume to verify Week 1 functionality without API keys:
```bash
export LLM_PROVIDER=mock
export EMBEDDING_BACKEND=hash
python -m talentlens.rag.index
```

Usage flow:
1. Upload a resume file via `/upload_resume`.
2. Read the returned `resume_id`.
3. Use that exact `resume_id` in `/chat` requests.

If an unknown `resume_id` is sent to `/chat`, the API returns `404` with a clear error message.

## Data Layout
```
data/
  kaggle_datasets.json
  raw/
    kaggle/
    policies/
    uploads/
  processed/
    resumes/
    jds/
  eval/
    golden_eval.json
  samples/
    resume_alex_johnson.txt
```

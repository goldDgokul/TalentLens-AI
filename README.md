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

### 6) Demo (sample resume)
Use the provided sample resume to verify Week 1 functionality without API keys:
```bash
export LLM_PROVIDER=mock
export EMBEDDING_BACKEND=hash
python -m talentlens.rag.index
```

Upload `data/samples/resume_alex_johnson.txt` via `/upload_resume`, then query `/chat` with factual questions. Citations are included in every response.

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

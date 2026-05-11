# TalentLens-AI
An Intelligent Recruitment Co-pilot Powered by Retrieval-Augmented Generation and Generative AI.

## Week 1 Setup (Resume-only RAG)

### 1) Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1.1) Install Ollama and pull llama3
1. Install Ollama from https://ollama.com/download
2. Start Ollama:
   ```bash
   ollama serve
   ```
3. Pull the default model:
   ```bash
   ollama pull llama3
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
# Ensure `ollama serve` is running in another terminal (or as a service).
# `ollama pull llama3` is only needed once per machine.
uvicorn main:app --reload
```

### Environment variables
- `LLM_PROVIDER` (optional, default: `ollama`): supports `ollama`, `mock`, and `none`.
- `OLLAMA_BASE_URL` (optional, default: `http://localhost:11434`)
- `OLLAMA_MODEL` (optional, default: `llama3`)
- `EMBEDDING_BACKEND` (optional, default: `sentence-transformers`): set to `hash` for lightweight local/demo runs.

### 6) Demo (sample resume)
Use the provided sample resume to verify Week 1 functionality with local Ollama:
```bash
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3
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

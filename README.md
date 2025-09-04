# Financial Document RAG + Knowledge Graph

**One-liner:** Retrieval over SEC filings/news with enterprise-style entity linking and a mini knowledge graph to ground LLM answers and reduce hallucinations.

## Why this matters
Map this repo to market pain points and regulations in its sector (see top-level report in the chat).

## Features
- [ ] Core pipeline (`src/pipeline.py`)
- [ ] Web API (`src/app.py`) with `/healthz`
- [ ] Vector/RAG or ML components (scaffolded)
- [ ] Observability: MLflow + logs (scaffolded)
- [ ] Governance: model cards / AI cards (templates)
- [ ] CI (`.github/workflows/ci.yml`), pre-commit

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python -m src.app --serve   # requires fastapi/uvicorn
python main.py --sum 1 2 3
```

## Project layout

```
.
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── requirements.txt
├── src
│   ├── app.py
│   ├── config.py
│   └── pipeline.py
├── tests
│   └── test_smoke.py
├── main.py
├── LICENSE
└── README.md
```

## Notes
- Imports of optional dependencies (FastAPI, FAISS, etc.) happen **inside functions** to keep imports lightweight.
- Replace the stubbed functions in `src/pipeline.py` with real logic and extend unit tests accordingly.
- Use `data/` for sample datasets (`data/.gitkeep` is included).

## License
Apache-2.0

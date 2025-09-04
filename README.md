# KYC Agent Factory

Agentic KYC/AML pipeline: **ingest → resolve name → sanctions & adverse‑media screening → risk scoring → human review**, with an **append‑only audit trail** and production‑minded structure (lazy imports, swappable storage, CI-ready).

---

## Core capabilities
- **Document ingestion** (IDs, proofs): normalizes and indexes uploaded artifacts
- **Name resolution**: canonicalizes names and estimates confidence (fuzzy matching)
- **Sanctions screening** (sample SDN list included)
- **Adverse media screening** (sample headlines + RAG helpers)
- **Risk scoring**: transparent 0–100 score + LOW/MEDIUM/HIGH band with reasons
- **Auditability**: append-only audit events for every stage
- **Extensibility**: optional FAISS/pgvector, LangChain/LlamaIndex, MLflow, Postgres (SQLAlchemy store)

---

## High‑impact use cases

1) **Retail/SME Onboarding (KYC)**
   - Intake government ID + business docs
   - Resolve legal name / beneficial owners
   - Screen against sanctions and adverse media
   - Produce **risk score** and decision: `AUTO‑APPROVE` vs `REVIEW`
   - **Artifacts:** case JSON, audit trail, risk rationale

2) **Periodic KYC Refresh (pKYC)**
   - Re-run screening on existing customers on a schedule or risk trigger
   - Compare risk deltas; escalate if band increased
   - Log pKYC event in audit history for model governance

3) **Enhanced Due Diligence (EDD) for High Risk**
   - Expand to more data sources (corporate registries, PEP lists, court records)
   - Lower decision thresholds; require human sign‑off
   - Generate an EDD summary (findings, links, timestamps)

4) **Correspondent Banking Counterparty Checks**
   - Run name resolution + sanctions on foreign FI names & key officers
   - Evidence links + audit timeline for compliance/internal audit

5) **Synthetic ID / Deepfake Risk Signal Integration**
   - Add external signals (document liveness, selfie liveness, device/IP anomalies)
   - Use **risk gates** to require manual review when signals trip
   - Keep a **traceable audit** of which guardrails blocked/allowed progression

6) **Adverse‑Media RAG**
   - Ingest curated news/policy corpus
   - Use `rag.py` to retrieve supporting snippets with **citations**
   - Attach citations to analyst view to reduce hallucinations

---

## Architecture (logical flow)

```
[Documents] → [Ingestion] → [Name Resolution] → [Sanctions Screen]
                               |                    |
                               v                    v
                          [Audit Log]        [Adverse Media Screen]
                               \              /
                                \            /
                                 → [Risk Scoring] → [Human Review Gate] → Decision
                                                 \→ [Audit Log + Case Artifacts]
```

**Modules**
- `ingestion.py` — normalize & index docs
- `resolution.py` — canonicalize name + confidence
- `screening.py` — sample sanctions/adverse media matching
- `risk.py` — transparent, explainable risk function
- `orchestrator.py` — end‑to‑end agent pipeline + audit hooks
- `storage.py` — JSONStore (default, portable); swap to SQLAlchemy later
- `rag.py` — FAISS retrieval (with stdlib fallback)

---

## How to run

### 0) Clone & (optional) create a virtual env
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt            # optional; repo runs without heavy deps
```

### 1) Run unit tests (pure stdlib)
```bash
pytest -q
```

### 2) CLI demo (no third‑party deps required)
```bash
python main.py
# → prints {"case_id": "...", "risk": {...}, "decision": "AUTO-APPROVE|REVIEW", ...}
```

### 3) Start the API (requires FastAPI & Uvicorn)
```bash
python -m kyc_agent_factory.app --serve
# GET http://localhost:8000/healthz
```

**Sample API flow**
```bash
# Create a case
curl -s -X POST http://localhost:8000/cases \
  -H "Content-Type: application/json" \
  -d '{"subject_name":"Alice Example","documents":[{"type":"passport","number":"X123"}]}'

# Run the pipeline on that case (replace <ID> with the returned id)
curl -s -X POST http://localhost:8000/cases/<ID>/run | jq .

# Get case with artifacts
curl -s http://localhost:8000/cases/<ID> | jq .

# Get audit trail
curl -s http://localhost:8000/reports/<ID> | jq .
```

### 4) Docker & Postgres (optional)
```bash
docker compose up --build
# App on :8000, Postgres on :5432 (user: postgres / pass: postgres / DB: kyc)
```

Set `DATABASE_URL` (in `compose.yaml` or env) to use Postgres with a SQLAlchemy store once implemented.

---

## Configuration

Environment variables:
- `DATABASE_URL` — e.g., `postgresql+psycopg2://user:pass@host:5432/kyc` (optional; JSONStore is default)
- `MLFLOW_TRACKING_URI` — to enable tracking (optional)
- `ENV` — `dev|prod` (optional)

---

## Data & evaluation

- **Sample data** shipped for quick screening demos: small SDN‑like names + adverse media headlines.
- For realistic runs, replace datasets in `src/kyc_agent_factory/screening.py` with:
  - OFAC/Consolidated sanctions lists
  - Curated adverse media feeds / knowledge base

**RAG quality:** use `rag.py` (FAISS if installed; stdlib fallback otherwise). Add an evaluation notebook for precision@k and citation coverage.

---

## Risk scoring (explainable)
- Weights sources transparently: sanctions > adverse media > name uncertainty > doc count
- Returns `score (0–100)`, `band (LOW|MEDIUM|HIGH)`, and `reasons`

---

## Compliance & audit
- Each step appends a structured event (`ts`, `action`, `details`) to an **append‑only audit** object that is persisted in storage.
- Use these logs for **model risk management** (e.g., SR 11‑7) and compliance reviews.

---

## Roadmap ideas
- Implement `SqlAlchemyStore` (DDL + migrations) and switch via `get_store()`
- Integrate MLflow runs & artifacts for each stage
- Add pgvector/FAISS‑backed adverse media store and retrieval evaluators
- Add policy‑gated guardrails and reviewer work queue
- Add real sanctions/PEP providers and identity/liveness signals

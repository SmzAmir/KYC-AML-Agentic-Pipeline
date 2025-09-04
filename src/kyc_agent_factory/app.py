from __future__ import annotations
import os, sys

def create_app():
    try:
        from fastapi import FastAPI
        from fastapi.responses import JSONResponse
        from pydantic import BaseModel
    except Exception:
        class Stub:
            def __init__(self): self.routes = []
        return Stub()

    from .orchestrator import Orchestrator
    from .storage import get_store

    class CaseCreate(BaseModel):
        subject_name: str
        documents: list | None = None

    store = get_store()
    orch = Orchestrator(store=store)
    app = FastAPI(title="KYC Agent Factory")

    @app.get("/healthz")
    def healthz(): return {"status": "ok"}

    @app.post("/cases")
    def create_case(payload: CaseCreate):
        cid = orch.create_case(payload.subject_name, payload.documents or [])
        return {"id": cid}

    @app.post("/cases/{case_id}/run")
    def run_case(case_id: str):
        report = orch.run_case(case_id)
        return JSONResponse(report)

    @app.get("/cases/{case_id}")
    def get_case(case_id: str): return orch.get_case(case_id)

    @app.get("/reports/{case_id}")
    def get_report(case_id: str): return orch.get_audit(case_id)

    return app

if __name__ == "__main__":
    if "--serve" in sys.argv:
        try:
            import uvicorn
            uvicorn.run(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
        except Exception:
            print("Install fastapi/uvicorn to serve API.")
    else:
        # CLI fallback
        from .orchestrator import Orchestrator
        from .storage import get_store
        import json
        orch = Orchestrator(get_store())
        cid = orch.create_case("Alice Example", [{"type": "passport", "number": "X123"}])
        print(json.dumps(orch.run_case(cid), indent=2))

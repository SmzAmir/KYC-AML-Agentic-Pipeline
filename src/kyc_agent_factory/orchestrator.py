from __future__ import annotations
from typing import Dict, Any, List
from .audit import AuditTrail
from .ingestion import ingest_documents
from .resolution import resolve_name
from .screening import sanctions_screen, adverse_media_screen, ScreeningHit
from .risk import score_risk
from .storage import get_store

class Orchestrator:
    def __init__(self, store=None):
        self.store = store or get_store()

    def create_case(self, subject_name: str, documents: List[Dict[str, Any]] | None = None) -> str:
        cid = self.store.create_case(subject_name, documents or [])
        # initial audit
        self.store.append_audit(cid, {"ts":"", "case_id":cid, "action":"case_created", "details":{"subject":subject_name}})
        return cid

    def run_case(self, cid: str) -> Dict[str, Any]:
        case = self.store.get_case(cid)
        if not case:
            raise ValueError("Case not found")

        audit = AuditTrail()

        # 1) Ingest
        ingest = ingest_documents(case.get("documents", []))
        audit.log(cid, "ingested_documents", ingest)

        # 2) Resolve name
        res = resolve_name(case["subject_name"])
        audit.log(cid, "name_resolved", {"input": res.input_name, "canonical": res.canonical_name, "confidence": res.confidence})

        # 3) Screen
        s_hits: List[ScreeningHit] = sanctions_screen(res.canonical_name)
        m_hits: List[ScreeningHit] = adverse_media_screen(res.canonical_name)
        audit.log(cid, "sanctions_screened", {"hits": [h.__dict__ for h in s_hits]})
        audit.log(cid, "adverse_media_screened", {"hits": [h.__dict__ for h in m_hits]})

        # 4) Risk scoring
        risk = score_risk(res.confidence, s_hits, m_hits, ingest["doc_count"])
        audit.log(cid, "risk_scored", risk)

        # 5) Human review placeholder (policy gate)
        decision = "REVIEW" if risk["band"] != "LOW" else "AUTO-APPROVE"
        audit.log(cid, "human_review_required", {"decision": decision})

        # Save artifacts
        case["status"] = "processed"
        case["artifacts"] = {
            "name_resolution": res.__dict__,
            "sanctions_hits": [h.__dict__ for h in s_hits],
            "adverse_media_hits": [h.__dict__ for h in m_hits],
            "risk": risk,
            "decision": decision,
        }
        self.store.save_case(cid, case)

        # persist audit
        for e in audit.events:
            self.store.append_audit(cid, e)

        return {"case_id": cid, "risk": risk, "decision": decision, "hits": {"sanctions": len(s_hits), "adverse_media": len(m_hits)}}

    def get_case(self, cid: str) -> Dict[str, Any]:
        return self.store.get_case(cid)

    def get_audit(self, cid: str) -> Dict[str, Any]:
        return self.store.get_audit(cid)

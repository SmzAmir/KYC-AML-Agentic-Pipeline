from __future__ import annotations
import os, json, uuid
from typing import Any, Dict

class JSONStore:
    """
    Simple file-backed store. Writes to src/kyc_agent_factory/.data/kyc_store.json
    so it works no matter the working directory.
    """
    def __init__(self, path: str | None = None):
        base = os.path.dirname(__file__)
        self.path = path or os.path.join(base, ".data", "kyc_store.json")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({"cases": {}, "audits": {}}, f)

    def _read(self) -> Dict[str, Any]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, obj: Dict[str, Any]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)

    def create_case(self, subject_name: str, documents: list) -> str:
        db = self._read()
        cid = str(uuid.uuid4())
        db["cases"][cid] = {
            "id": cid,
            "subject_name": subject_name,
            "documents": documents,
            "status": "created",
            "artifacts": {},
        }
        db["audits"][cid] = {"events": []}
        self._write(db)
        return cid

    def get_case(self, cid: str) -> Dict[str, Any] | None:
        return self._read()["cases"].get(cid)

    def save_case(self, cid: str, case: Dict[str, Any]) -> None:
        db = self._read()
        db["cases"][cid] = case
        self._write(db)

    def append_audit(self, cid: str, event: Dict[str, Any]):
        db = self._read()
        db.setdefault("audits", {}).setdefault(cid, {"events": []})["events"].append(event)
        self._write(db)

    def get_audit(self, cid: str) -> Dict[str, Any]:
        return self._read()["audits"].get(cid, {"events": []})

def get_store():
    # For prod, swap to SqlAlchemyStore (see storage_sqlalchemy.py)
    return JSONStore()

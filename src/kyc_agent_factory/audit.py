from __future__ import annotations
import time
from typing import Any, Dict, List

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

class AuditTrail:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def log(self, case_id: str, action: str, details: Dict[str, Any] | None = None):
        self.events.append({
            "ts": now_iso(),
            "case_id": case_id,
            "action": action,
            "details": details or {},
        })

    def to_dict(self) -> Dict[str, Any]:
        return {"events": self.events}

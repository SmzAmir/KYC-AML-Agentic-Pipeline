from __future__ import annotations
from typing import Dict, Any, List
from .screening import ScreeningHit

def score_risk(resolution_conf: float, sanctions: List[ScreeningHit], media: List[ScreeningHit], doc_count: int) -> Dict[str, Any]:
    base = 10
    base += int((1 - resolution_conf) * 20)          # name uncertainty
    base += 50 if sanctions else 0                    # sanctions = high weight
    base += 20 if len(media) >= 2 else 10 if media else 0
    base += 5 if doc_count == 0 else 0
    score = max(0, min(100, base))
    band = "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW"
    reasons = []
    if sanctions: reasons.append("sanctions_match")
    if media: reasons.append("adverse_media")
    if resolution_conf < 0.9: reasons.append("name_uncertainty")
    if doc_count == 0: reasons.append("no_docs")
    return {"score": score, "band": band, "reasons": reasons}

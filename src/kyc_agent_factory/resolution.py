from __future__ import annotations
import difflib
from dataclasses import dataclass

@dataclass
class NameResolution:
    input_name: str
    canonical_name: str
    confidence: float

def resolve_name(name: str) -> NameResolution:
    canonical = " ".join(w.capitalize() for w in name.split())
    conf = difflib.SequenceMatcher(None, name.lower(), canonical.lower()).ratio()
    return NameResolution(input_name=name, canonical_name=canonical, confidence=conf)

from __future__ import annotations
import os, csv, json, difflib
from typing import List
from dataclasses import dataclass

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Create tiny sample datasets on first import (idempotent)
_sdn_path = os.path.join(DATA_DIR, "sdn_sample.csv")
if not os.path.exists(_sdn_path):
    with open(_sdn_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["name"])
        w.writerow(["John Example"]); w.writerow(["Alice Example"]); w.writerow(["Evil Corp Beneficial Owner"])

_media_path = os.path.join(DATA_DIR, "adverse_media_sample.jsonl")
if not os.path.exists(_media_path):
    with open(_media_path, "w", encoding="utf-8") as f:
        f.write(json.dumps({"title":"Alice Example linked to controversy"}) + "\n")
        f.write(json.dumps({"title":"Report: John Example involved in inquiry"}) + "\n")

@dataclass
class ScreeningHit:
    source: str
    query: str
    match: str
    score: float

def _read_sdn() -> List[str]:
    with open(_sdn_path, newline="", encoding="utf-8") as f:
        return [row[0] for row in csv.reader(f)][1:]

def _read_adverse_media() -> List[str]:
    lines = []
    with open(_media_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                lines.append(obj.get("title", ""))
            except Exception:
                continue
    return lines

def sanctions_screen(name: str) -> List[ScreeningHit]:
    names = _read_sdn()
    hits: List[ScreeningHit] = []
    for entry in names:
        score = difflib.SequenceMatcher(None, name.lower(), entry.lower()).ratio()
        if score >= 0.85:
            hits.append(ScreeningHit(source="OFAC_SDN_SAMPLE", query=name, match=entry, score=score))
    return hits

def adverse_media_screen(name: str) -> List[ScreeningHit]:
    titles = _read_adverse_media()
    hits: List[ScreeningHit] = []
    for t in titles:
        score = difflib.SequenceMatcher(None, name.lower(), t.lower()).ratio()
        if score >= 0.65 and name.lower() in t.lower():
            hits.append(ScreeningHit(source="ADVERSE_MEDIA_SAMPLE", query=name, match=t, score=score))
    return hits

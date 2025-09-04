from __future__ import annotations
from typing import List, Dict, Any

def ingest_documents(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    index: Dict[str, list] = {}
    for doc in documents or []:
        dtype = str(doc.get("type", "unknown")).lower()
        index.setdefault(dtype, []).append(doc)
    return {"doc_index": index, "doc_count": sum(len(v) for v in index.values())}

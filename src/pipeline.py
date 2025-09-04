"""Core pipeline primitives for Financial Document RAG + Knowledge Graph.
These functions avoid third-party imports at import-time so unit tests pass even without internet.
"""
from __future__ import annotations
import os
import json
from typing import Dict, Any, List

def healthcheck() -> Dict[str, str]:
    """Simple health check used by smoke tests."""
    return {"service": "fin-doc-rag-kg", "status": "ok"}

def example_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Example pure-Python task. Replace with domain logic."""
    # Simulate a small computation
    total = sum(v for v in payload.values() if isinstance(v, (int, float)))
    return {"input_keys": list(payload.keys()), "numeric_total": total}

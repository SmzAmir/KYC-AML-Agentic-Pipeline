# Optional retrieval helpers; fall back to stdlib if FAISS unavailable.
from __future__ import annotations
from typing import List, Tuple

def simple_retrieve(query: str, corpus: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    import difflib
    scored = [(t, difflib.SequenceMatcher(None, query.lower(), t.lower()).ratio()) for t in corpus]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:top_k]

def faiss_retrieve_or_fallback(query: str, corpus: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    try:
        import numpy as np, faiss
        from numpy.linalg import norm
        vocab = sorted({w for text in corpus+[query] for w in text.lower().split()})
        def embed(t: str):
            v = [t.lower().split().count(w) for w in vocab]
            import numpy as np
            arr = np.array(v, dtype="float32")
            n = norm(arr)
            return arr if n == 0 else (arr / n)
        X = np.vstack([embed(t) for t in corpus]).astype("float32")
        index = faiss.IndexFlatIP(X.shape[1]); index.add(X)
        q = embed(query).reshape(1, -1).astype("float32")
        D, I = index.search(q, min(top_k, len(corpus)))
        return [(corpus[i], float(D[0][k])) for k, i in enumerate(I[0])]
    except Exception:
        return simple_retrieve(query, corpus, top_k)

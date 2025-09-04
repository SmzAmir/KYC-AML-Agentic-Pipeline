from __future__ import annotations
from typing import Any, Dict
from .config import settings

class SqlAlchemyStore:
    """
    Optional, minimal sketch for Postgres/SQLAlchemy storage.
    Not used by default. Implement models/migrations if you want to enable.
    """
    def __init__(self, url: str | None = None):
        try:
            from sqlalchemy import create_engine, text
        except Exception as e:
            raise RuntimeError("SQLAlchemy not installed") from e
        self.engine = create_engine(url or settings.database_url, future=True)
        # You would also create tables (cases, audits) via metadata.create_all()

    def create_case(self, subject_name: str, documents: list) -> str:
        # Implement insert; return generated UUID
        raise NotImplementedError

    def get_case(self, cid: str) -> Dict[str, Any] | None:
        raise NotImplementedError

    def save_case(self, cid: str, case: Dict[str, Any]) -> None:
        raise NotImplementedError

    def append_audit(self, cid: str, event: Dict[str, Any]):
        raise NotImplementedError

    def get_audit(self, cid: str) -> Dict[str, Any]:
        raise NotImplementedError

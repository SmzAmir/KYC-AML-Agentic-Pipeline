import os
from dataclasses import dataclass

@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///local.db")
    env: str = os.getenv("ENV", "dev")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "")

settings = Settings()

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    france_travail_api_key: str | None = os.getenv("FRANCE_TRAVAIL_API_KEY")
    adzuna_app_id: str | None = os.getenv("ADZUNA_APP_ID")
    adzuna_app_key: str | None = os.getenv("ADZUNA_APP_KEY")
    eures_api_key: str | None = os.getenv("EURES_API_KEY")
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")

    # DB/infra (remplaçable par Postgres/pgvector)
    database_url: str = os.getenv("DATABASE_URL", "memory://jobs")


settings = Settings()


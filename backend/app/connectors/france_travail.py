from __future__ import annotations

from typing import List

from ..models import JobPosting


def fetch_jobs(query: str, limit: int = 20) -> List[JobPosting]:
    """
    Placeholder France Travail connector.
    A remplacer par l'appel API officielle (OAuth + endpoint offres).
    """
    sample = JobPosting(
        id="fr-travail-1",
        source="france_travail",
        source_job_id="stub-1",
        title="Développeur Python FastAPI",
        company="Exemple SA",
        country="FR",
        city="Paris",
        remote_type="hybrid",
        contract_type="CDI",
        salary_min=45000,
        salary_max=55000,
        currency="EUR",
        salary_period="year",
        description="Projet API data, FastAPI, Postgres, CI/CD.",
        skills=["python", "fastapi", "postgres"],
        apply_url="https://francetravail.example/apply/stub-1",
    )
    return [sample][:limit]


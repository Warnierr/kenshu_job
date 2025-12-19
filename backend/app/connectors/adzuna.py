from __future__ import annotations

from typing import List

from ..models import JobPosting


def fetch_jobs(query: str, country: str = "fr", limit: int = 20) -> List[JobPosting]:
    """
    Placeholder Adzuna connector.
    A remplacer par l'appel API REST (app_id + app_key, endpoint /jobs/{country}/search/1).
    """
    sample = JobPosting(
        id=f"adzuna-{country}-1",
        source="adzuna",
        source_job_id="stub-1",
        title="Backend Engineer (Remote Europe)",
        company="RemoteCorp",
        country=country.upper(),
        city=None,
        remote_type="remote",
        contract_type="Permanent",
        salary_min=60000,
        salary_max=80000,
        currency="EUR",
        salary_period="year",
        description="Python, FastAPI, AWS, data pipelines.",
        skills=["python", "fastapi", "aws"],
        apply_url="https://adzuna.example/apply/stub-1",
    )
    return [sample][:limit]


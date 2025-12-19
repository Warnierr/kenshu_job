from __future__ import annotations

from typing import List

from ..models import JobPosting


def fetch_jobs(query: str, country: str | None = None, limit: int = 20) -> List[JobPosting]:
    """
    Placeholder EURES connector.
    A remplacer par l'intégration EURES (API ou flux partenaire).
    """
    sample = JobPosting(
        id=f"eures-{country or 'eu'}-1",
        source="eures",
        source_job_id="stub-1",
        title="Data Engineer Europe (Hybrid)",
        company="EuroData",
        country=country.upper() if country else "EU",
        city="Bruxelles",
        remote_type="hybrid",
        contract_type="Permanent",
        salary_min=None,
        salary_max=None,
        currency="EUR",
        salary_period="year",
        description="Spark, Python, cloud; anglais requis.",
        skills=["python", "spark", "cloud"],
        apply_url="https://eures.example/apply/stub-1",
    )
    return [sample][:limit]


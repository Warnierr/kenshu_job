from __future__ import annotations

from typing import List

from ..connectors import (
    fetch_adzuna,
    fetch_apec,
    fetch_eures,
    fetch_france_travail,
    fetch_indeed,
    fetch_scraping,
)
from ..models import JobPosting, SearchRequest
from ..storage.memory import store
from ..utils.dedupe import deduplicate
from ..utils.scoring import score_job


class Pipeline:
    def harvest(self, req: SearchRequest) -> List[JobPosting]:
        query = " ".join(req.keywords) if req.keywords else "developpeur"
        country = req.countries[0] if req.countries else "fr"
        jobs: List[JobPosting] = []
        
        # APIs (stubs)
        jobs.extend(fetch_france_travail(query))
        jobs.extend(fetch_adzuna(query, country=country))
        jobs.extend(fetch_eures(query, country=country))
        
        # Scraping actif
        jobs.extend(fetch_scraping(query, country=country))
        
        # APEC (France uniquement)
        if country == "fr":
            jobs.extend(fetch_apec(query, limit=15))
        
        # Indeed (avec location)
        location = "France" if country == "fr" else country.upper()
        jobs.extend(fetch_indeed(query, location=location, limit=15))
        
        unique = deduplicate(jobs)
        store.upsert_jobs(unique)
        return unique

    def search(self, req: SearchRequest) -> List[JobPosting]:
        # In real impl: vector search + filtres SQL; ici in-memory
        jobs = store.search()
        scored = [score_job(job, req) for job in jobs]
        scored.sort(key=lambda j: j.match_score or 0, reverse=True)
        return scored


pipeline = Pipeline()


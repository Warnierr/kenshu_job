from __future__ import annotations

from typing import Dict, List

from ..models import JobPosting


class MemoryStore:
    def __init__(self) -> None:
        self._jobs: Dict[str, JobPosting] = {}

    def upsert_jobs(self, jobs: List[JobPosting]) -> int:
        for job in jobs:
            self._jobs[job.id] = job
        return len(jobs)

    def search(self) -> List[JobPosting]:
        return list(self._jobs.values())

    def clear(self) -> None:
        self._jobs = {}


store = MemoryStore()


from __future__ import annotations

import hashlib
from typing import Iterable, List

from ..models import JobPosting


def compute_hash(job: JobPosting) -> str:
    key = "|".join(
        [
            (job.source or "").lower(),
            (job.title or "").lower(),
            (job.company or "").lower(),
            (job.city or "").lower(),
        ]
    )
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def deduplicate(jobs: Iterable[JobPosting]) -> List[JobPosting]:
    seen = set()
    unique: List[JobPosting] = []
    for job in jobs:
        h = compute_hash(job)
        if h in seen:
            continue
        seen.add(h)
        unique.append(job)
    return unique


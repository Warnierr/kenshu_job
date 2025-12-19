from __future__ import annotations

import math
from typing import List, Optional

from ..models import JobPosting, SearchRequest


def _normalize(text: Optional[str]) -> str:
    return (text or "").lower()


def keyword_score(keywords: List[str], text: str) -> float:
    if not keywords:
        return 0.0
    text_l = text.lower()
    hits = sum(1 for kw in keywords if kw.lower() in text_l)
    return hits / len(keywords)


def constraint_penalty(job: JobPosting, req: SearchRequest) -> float:
    penalty = 0.0
    if req.remote_preference and job.remote_type and req.remote_preference != job.remote_type:
        penalty += 0.2
    if req.contract_types and job.contract_type:
        if job.contract_type.lower() not in [c.lower() for c in req.contract_types]:
            penalty += 0.2
    if req.countries and job.country:
        if job.country.lower() not in [c.lower() for c in req.countries]:
            penalty += 0.2
    if req.salary_min and job.salary_min and job.salary_min < req.salary_min:
        penalty += 0.2
    return penalty


def score_job(job: JobPosting, req: SearchRequest) -> JobPosting:
    title_desc = f"{job.title} {job.description or ''}"
    kw_score = keyword_score(req.keywords, title_desc)
    cv_score = keyword_score(req.keywords, " ".join(req.languages) + " " + (req.cv_summary or ""))
    base = max(kw_score, cv_score)
    penalties = constraint_penalty(job, req)
    score = max(0.0, min(1.0, base - penalties))
    job.match_score = round(score, 3)
    reasons: List[str] = []
    if kw_score > 0:
        reasons.append(f"Mots-clés trouvés ({math.ceil(kw_score*100)}%)")
    if req.remote_preference:
        reasons.append(f"Remote attendu: {req.remote_preference}, offre: {job.remote_type or 'n/a'}")
    if req.contract_types:
        reasons.append(f"Contrat cible: {', '.join(req.contract_types)}")
    job.reasons = reasons
    return job


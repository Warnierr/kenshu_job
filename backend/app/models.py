from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class JobPosting(BaseModel):
    id: str
    source: str
    source_job_id: str
    title: str
    company: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    remote_type: Optional[str] = Field(
        default=None, description="remote|hybrid|onsite|unknown"
    )
    contract_type: Optional[str] = None
    experience_level: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    salary_period: Optional[str] = Field(
        default=None, description="year|month|day|hour|unknown"
    )
    salary_confidence: Optional[float] = Field(
        default=None, description="0..1 confiance sur l'extraction salaire"
    )
    description: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    posted_at: Optional[datetime] = None
    apply_url: Optional[str] = None
    match_score: Optional[float] = Field(
        default=None, description="Score final CV↔offre, 0..1"
    )
    reasons: List[str] = Field(default_factory=list)


class SearchRequest(BaseModel):
    keywords: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
    countries: List[str] = Field(default_factory=list)
    contract_types: List[str] = Field(default_factory=list)
    remote_preference: Optional[str] = Field(
        default=None, description="remote|hybrid|onsite"
    )
    salary_min: Optional[float] = None
    languages: List[str] = Field(default_factory=list)
    exclusions: List[str] = Field(default_factory=list)
    cv_summary: Optional[str] = Field(
        default=None, description="Résumé texte du CV (compétences, secteurs, années)"
    )


class SearchResponse(BaseModel):
    total: int
    items: List[JobPosting]



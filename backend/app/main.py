from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .api import profile as profile_api
from .models import SearchRequest, SearchResponse
from .services.pipeline import pipeline

app = FastAPI(title="Job Search Engine", version="0.1.0")

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(profile_api.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest", response_model=SearchResponse)
def ingest(req: SearchRequest):
    jobs = pipeline.harvest(req)
    return SearchResponse(total=len(jobs), items=jobs)


@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest, user_id: str | None = Query(None, description="ID utilisateur pour utiliser le profil sauvegardé")):
    """Recherche d'emploi avec option d'utiliser le profil utilisateur."""
    from ..storage.profile_store import profile_store
    
    # Si user_id fourni, charger le profil et enrichir la requête
    if user_id:
        profile = profile_store.get(user_id)
        if profile:
            # Utiliser le profil pour enrichir la recherche
            if not req.cv_summary and profile.to_cv_summary():
                req.cv_summary = profile.to_cv_summary()
            
            # Utiliser les préférences du profil si non spécifiées
            if not req.contract_types and profile.preferred_contract_types:
                req.contract_types = profile.preferred_contract_types
            
            if not req.remote_preference and profile.preferred_remote:
                req.remote_preference = profile.preferred_remote
            
            if not req.salary_min and profile.salary_min:
                req.salary_min = profile.salary_min
            
            if not req.countries and profile.preferred_countries:
                req.countries = profile.preferred_countries
    
    jobs = pipeline.search(req)
    return SearchResponse(total=len(jobs), items=jobs)


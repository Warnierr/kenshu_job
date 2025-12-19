from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest", response_model=SearchResponse)
def ingest(req: SearchRequest):
    jobs = pipeline.harvest(req)
    return SearchResponse(total=len(jobs), items=jobs)


@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    jobs = pipeline.search(req)
    return SearchResponse(total=len(jobs), items=jobs)


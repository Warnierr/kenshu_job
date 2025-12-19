"""
Scrapeur hebdomadaire pour alimenter la BDD.

Tourne en tâche de fond (cron/Celery/APScheduler) et :
1. Scrape toutes les sources configurées
2. Normalise et déduplique
3. Stocke en BDD
4. Enrichit (salaire/remote/skills)

Usage:
    python -m app.scheduler.weekly_scraper
"""
from __future__ import annotations

import os
from datetime import datetime
from typing import List

from ..connectors import (
    fetch_adzuna,
    fetch_eures,
    fetch_france_travail,
    fetch_scraping,
)
from ..connectors.apec import fetch_jobs as fetch_apec
from ..connectors.indeed import fetch_jobs as fetch_indeed
from ..models import JobPosting
from ..storage.memory import store
from ..utils.dedupe import deduplicate


# Configuration des requêtes à lancer chaque semaine
WEEKLY_QUERIES = [
    # Dev
    {"keywords": "python developer", "countries": ["fr"]},
    {"keywords": "javascript react", "countries": ["fr"]},
    {"keywords": "java spring", "countries": ["fr"]},
    {"keywords": "golang developer", "countries": ["fr"]},
    {"keywords": "rust developer", "countries": ["fr", "de", "us"]},
    
    # Mobile
    {"keywords": "react native", "countries": ["fr"]},
    {"keywords": "flutter developer", "countries": ["fr"]},
    {"keywords": "ios swift", "countries": ["fr"]},
    {"keywords": "android kotlin", "countries": ["fr"]},
    
    # DevOps/Cloud
    {"keywords": "devops kubernetes", "countries": ["fr"]},
    {"keywords": "sre site reliability", "countries": ["fr", "de"]},
    {"keywords": "cloud architect aws", "countries": ["fr"]},
    {"keywords": "terraform ansible", "countries": ["fr"]},
    
    # Data/AI
    {"keywords": "data engineer", "countries": ["fr"]},
    {"keywords": "data scientist", "countries": ["fr"]},
    {"keywords": "machine learning engineer", "countries": ["fr", "de"]},
    {"keywords": "mlops", "countries": ["fr"]},
    
    # Autres
    {"keywords": "security engineer", "countries": ["fr"]},
    {"keywords": "qa test automation", "countries": ["fr"]},
    {"keywords": "blockchain developer", "countries": ["fr", "de"]},
    {"keywords": "game developer unity", "countries": ["fr"]},
]


class WeeklyScraper:
    """Scrapeur hebdomadaire."""
    
    def __init__(self):
        self.total_scraped = 0
        self.total_stored = 0
        self.errors = []
    
    def run(self):
        """Lance le scraping complet."""
        print(f"[WeeklyScraper] Starting at {datetime.now()}")
        
        for query_config in WEEKLY_QUERIES:
            try:
                self._scrape_query(query_config)
            except Exception as e:
                self.errors.append(f"Query {query_config}: {e}")
                print(f"[WeeklyScraper] Error: {e}")
        
        print(f"[WeeklyScraper] Finished!")
        print(f"  - Total scraped: {self.total_scraped}")
        print(f"  - Total stored: {self.total_stored}")
        print(f"  - Errors: {len(self.errors)}")
        
        return {
            "scraped": self.total_scraped,
            "stored": self.total_stored,
            "errors": self.errors,
        }
    
    def _scrape_query(self, config: dict):
        """Scrape une requête spécifique."""
        keywords = config["keywords"]
        countries = config.get("countries", ["fr"])
        country = countries[0]
        
        print(f"[WeeklyScraper] Scraping: {keywords} ({country})")
        
        jobs: List[JobPosting] = []
        
        # 1. API stubs (France Travail, Adzuna, EURES)
        try:
            jobs.extend(fetch_france_travail(keywords))
        except Exception as e:
            print(f"  [FT] {e}")
        
        try:
            jobs.extend(fetch_adzuna(keywords, country=country))
        except Exception as e:
            print(f"  [Adzuna] {e}")
        
        try:
            jobs.extend(fetch_eures(keywords, country=country))
        except Exception as e:
            print(f"  [EURES] {e}")
        
        # 2. Scraping générique (WTTJ, Remotive)
        try:
            jobs.extend(fetch_scraping(keywords, country=country))
        except Exception as e:
            print(f"  [Scraping] {e}")
        
        # 3. APEC (cadres France)
        if country == "fr":
            try:
                jobs.extend(fetch_apec(keywords, limit=15))
            except Exception as e:
                print(f"  [APEC] {e}")
        
        # 4. Indeed (avec délai pour éviter rate limit)
        try:
            location = "France" if country == "fr" else country.upper()
            jobs.extend(fetch_indeed(keywords, location=location, limit=15))
        except Exception as e:
            print(f"  [Indeed] {e}")
        
        self.total_scraped += len(jobs)
        
        # 5. Déduplication
        unique_jobs = deduplicate(jobs)
        
        # 6. Stockage
        store.upsert_jobs(unique_jobs)
        self.total_stored += len(unique_jobs)
        
        print(f"  → {len(jobs)} scraped, {len(unique_jobs)} unique")


def run_weekly_scraper():
    """Point d'entrée pour lancer le scraper."""
    scraper = WeeklyScraper()
    return scraper.run()


if __name__ == "__main__":
    # Lancement direct
    result = run_weekly_scraper()
    print("\n=== SUMMARY ===")
    print(f"Scraped: {result['scraped']}")
    print(f"Stored: {result['stored']}")
    if result['errors']:
        print(f"Errors: {len(result['errors'])}")
        for err in result['errors'][:5]:
            print(f"  - {err}")


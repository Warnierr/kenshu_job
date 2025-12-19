from .adzuna import fetch_jobs as fetch_adzuna
from .apec import fetch_jobs as fetch_apec
from .eures import fetch_jobs as fetch_eures
from .france_travail import fetch_jobs as fetch_france_travail
from .indeed import fetch_jobs as fetch_indeed
from .scraper import fetch_scraping

__all__ = [
    "fetch_france_travail",
    "fetch_adzuna",
    "fetch_eures",
    "fetch_scraping",
    "fetch_apec",
    "fetch_indeed",
]


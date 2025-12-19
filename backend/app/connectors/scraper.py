"""
Connecteur scraping générique pour sites d'emploi IT publics.
"""
from __future__ import annotations

import re
from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from ..models import JobPosting


def fetch_scraping(query: str, country: str = "fr") -> List[JobPosting]:
    """
    Scrape plusieurs sources publiques : Welcome to the Jungle, Remotive, etc.
    Mode simpliste : récupère titre/entreprise/lien depuis pages de résultat.
    """
    jobs: List[JobPosting] = []
    
    # 1) Welcome to the Jungle (France)
    if country == "fr":
        jobs.extend(_scrape_wttj(query))
    
    # 2) Remotive (remote international)
    jobs.extend(_scrape_remotive(query))
    
    return jobs


def _scrape_wttj(query: str) -> List[JobPosting]:
    """Welcome to the Jungle - scraping basique."""
    jobs = []
    try:
        url = f"https://www.welcometothejungle.com/fr/jobs?query={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return jobs
        
        soup = BeautifulSoup(res.text, "html.parser")
        # WTTJ structure change souvent, ici on fait du parsing simpliste
        # En pratique, il faut analyser le DOM réel
        job_cards = soup.select("li[data-testid='job-list-item']") or soup.select(".job-card")
        
        for idx, card in enumerate(job_cards[:10]):  # limite à 10
            title_el = card.select_one("h3, .job-title")
            company_el = card.select_one(".company-name, [data-testid='company-name']")
            link_el = card.select_one("a[href*='/jobs/']")
            
            title = title_el.get_text(strip=True) if title_el else f"Job WTTJ {idx}"
            company = company_el.get_text(strip=True) if company_el else "WTTJ Entreprise"
            href = link_el.get("href", "") if link_el else ""
            apply_url = f"https://www.welcometothejungle.com{href}" if href.startswith("/") else href
            
            jobs.append(
                JobPosting(
                    id=f"wttj-{idx}",
                    source="welcometothejungle",
                    source_job_id=f"wttj-{idx}",
                    title=title,
                    company=company,
                    country="fr",
                    city="Paris",  # placeholder
                    remote_type="hybrid",
                    contract_type="CDI",
                    apply_url=apply_url or "https://www.welcometothejungle.com",
                    description=f"Offre {title} chez {company}",
                )
            )
    except Exception as e:
        print(f"[WTTJ scrape error] {e}")
    return jobs


def _scrape_remotive(query: str) -> List[JobPosting]:
    """Remotive.io - jobs remote internationaux."""
    jobs = []
    try:
        url = f"https://remotive.io/remote-jobs/search?query={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return jobs
        
        soup = BeautifulSoup(res.text, "html.parser")
        job_cards = soup.select(".job-tile") or soup.select("li.job-list-item")
        
        for idx, card in enumerate(job_cards[:15]):
            title_el = card.select_one(".job-tile-title, h3")
            company_el = card.select_one(".company, .job-tile-company")
            link_el = card.select_one("a")
            
            title = title_el.get_text(strip=True) if title_el else f"Remote Job {idx}"
            company = company_el.get_text(strip=True) if company_el else "Remote Company"
            href = link_el.get("href", "") if link_el else ""
            apply_url = f"https://remotive.io{href}" if href.startswith("/") else href
            
            # parsing salaire basique si présent
            salary_text = card.get_text()
            salary_min, salary_max = _extract_salary(salary_text)
            
            jobs.append(
                JobPosting(
                    id=f"remotive-{idx}",
                    source="remotive",
                    source_job_id=f"remotive-{idx}",
                    title=title,
                    company=company,
                    country="international",
                    remote_type="remote",
                    contract_type="CDI",
                    salary_min=salary_min,
                    salary_max=salary_max,
                    currency="USD" if salary_min else None,
                    salary_period="year" if salary_min else None,
                    apply_url=apply_url or "https://remotive.io",
                    description=f"{title} @ {company}",
                )
            )
    except Exception as e:
        print(f"[Remotive scrape error] {e}")
    return jobs


def _extract_salary(text: str) -> tuple[int | None, int | None]:
    """Parse salaire depuis texte (ex: '$80k-$120k', '50000-70000€')."""
    # patterns basiques
    match = re.search(r"[\$€]?(\d+)k?\s*[-–]\s*[\$€]?(\d+)k?", text, re.IGNORECASE)
    if match:
        low = int(match.group(1))
        high = int(match.group(2))
        # si "k" présent, multiplier par 1000
        if "k" in text.lower():
            low *= 1000
            high *= 1000
        return (low, high)
    return (None, None)


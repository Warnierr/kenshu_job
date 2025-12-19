"""
Connecteur Indeed
Scraping du site https://fr.indeed.com

Note: Indeed a des protections anti-bot robustes.
Pour production, considérer:
- Rotating proxies
- Headers réalistes
- Délais entre requêtes
- Ou utiliser Indeed Publisher API (payante)
"""
from __future__ import annotations

import re
import time
from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from ..models import JobPosting


def fetch_jobs(query: str, location: str = "France", limit: int = 20) -> List[JobPosting]:
    """
    Scrape Indeed France.
    
    Args:
        query: mots-clés recherche
        location: localisation (ex: "Paris", "France", "Ile-de-France")
        limit: nombre max d'offres
    """
    jobs = []
    try:
        # URL Indeed France
        base_url = "https://fr.indeed.com/jobs"
        params = {
            "q": query,
            "l": location,
            "sort": "date",  # Trier par date (plus récent)
        }
        
        # Headers réalistes pour éviter blocage
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
        }
        
        # Construire URL
        query_string = "&".join([f"{k}={quote_plus(str(v))}" for k, v in params.items()])
        url = f"{base_url}?{query_string}"
        
        # Petit délai pour être sympa
        time.sleep(1)
        
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            print(f"[Indeed] Status {res.status_code}")
            return jobs
        
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Indeed structure (décembre 2024, peut changer):
        # Les offres sont dans des divs avec attribut data-jk (job key)
        job_cards = soup.select("div.job_seen_beacon, div[data-jk], td.resultContent")
        
        if not job_cards:
            # Fallback: chercher par classe
            job_cards = soup.find_all("div", class_=re.compile(r"(jobsearch-SerpJobCard|job_seen)", re.I))
        
        for idx, card in enumerate(job_cards[:limit]):
            try:
                # Job key (ID Indeed)
                job_key = card.get("data-jk", f"indeed-{idx}")
                
                # Titre
                title_el = card.select_one("h2 a span, h2.jobTitle span, a.jcs-JobTitle")
                if not title_el:
                    title_el = card.find("h2")
                title = title_el.get_text(strip=True) if title_el else f"Offre Indeed {idx}"
                
                # Entreprise
                company_el = card.select_one("span.companyName, div.company, span[data-testid='company-name']")
                company = company_el.get_text(strip=True) if company_el else "Entreprise"
                
                # Localisation
                location_el = card.select_one("div.companyLocation, div.location, span.companyLocation")
                location_text = location_el.get_text(strip=True) if location_el else location
                city = location_text.split(",")[0].strip() if location_text else "France"
                
                # Lien vers offre
                link_el = card.select_one("h2 a, a.jcs-JobTitle, a[data-jk]")
                href = link_el.get("href", "") if link_el else ""
                apply_url = f"https://fr.indeed.com{href}" if href.startswith("/") else href or f"https://fr.indeed.com/viewjob?jk={job_key}"
                
                # Description/snippet
                desc_el = card.select_one("div.job-snippet, div.summary, td.snippetColumn")
                description = desc_el.get_text(strip=True)[:250] if desc_el else f"{title} chez {company}"
                
                # Salaire (Indeed affiche parfois)
                salary_el = card.select_one("span.salary-snippet, div.salary-snippet-container, span.estimated-salary")
                salary_text = salary_el.get_text() if salary_el else card.get_text()
                salary_min, salary_max = _extract_salary_indeed(salary_text)
                
                # Remote
                remote_type = "onsite"
                text_lower = card.get_text().lower()
                if "télétravail" in text_lower or "remote" in text_lower or "100 % télétravail" in text_lower:
                    remote_type = "remote"
                elif "hybride" in text_lower or "partiel" in text_lower:
                    remote_type = "hybrid"
                
                # Type de contrat
                contract_type = "CDI"
                text_upper = card.get_text().upper()
                if "CDD" in text_upper or "TEMPS PLEIN - CDD" in text_upper:
                    contract_type = "CDD"
                elif "STAGE" in text_upper or "INTERN" in text_upper:
                    contract_type = "Internship"
                elif "FREELANCE" in text_upper or "INDÉPENDANT" in text_upper:
                    contract_type = "Freelance"
                
                jobs.append(
                    JobPosting(
                        id=f"indeed-{job_key}",
                        source="indeed",
                        source_job_id=job_key,
                        title=title,
                        company=company,
                        country="fr",
                        city=city,
                        remote_type=remote_type,
                        contract_type=contract_type,
                        salary_min=salary_min,
                        salary_max=salary_max,
                        currency="EUR" if salary_min else None,
                        salary_period="year" if salary_min else None,
                        apply_url=apply_url,
                        description=description,
                    )
                )
            except Exception as e:
                print(f"[Indeed] Error parsing card {idx}: {e}")
                continue
        
        print(f"[Indeed] Scraped {len(jobs)} jobs")
    
    except Exception as e:
        print(f"[Indeed] Global error: {e}")
    
    return jobs


def _extract_salary_indeed(text: str) -> tuple[int | None, int | None]:
    """
    Parse salaire depuis texte Indeed.
    Formats: "30 000 € - 45 000 € par an", "40K-50K", "25€/heure"
    """
    # Pattern 1: 30 000 € - 45 000 € par an
    match = re.search(r"(\d+)\s*000\s*€?\s*[-–]\s*(\d+)\s*000", text)
    if match:
        return (int(match.group(1)) * 1000, int(match.group(2)) * 1000)
    
    # Pattern 2: 30K-45K
    match = re.search(r"(\d+)\s*k[€]?\s*[-–]\s*(\d+)\s*k", text, re.IGNORECASE)
    if match:
        return (int(match.group(1)) * 1000, int(match.group(2)) * 1000)
    
    # Pattern 3: 25€/heure → convertir en annuel (35h/semaine * 52)
    match = re.search(r"(\d+)[,.]?(\d*)\s*€\s*/\s*heure", text, re.IGNORECASE)
    if match:
        hourly = int(match.group(1))
        annual = hourly * 35 * 52  # Approximation
        return (annual, annual)
    
    # Pattern 4: single value "45 000 €"
    match = re.search(r"(\d+)\s*000\s*€", text)
    if match:
        val = int(match.group(1)) * 1000
        return (val, val)
    
    return (None, None)


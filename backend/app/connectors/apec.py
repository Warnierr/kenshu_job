"""
Connecteur APEC (Association Pour l'Emploi des Cadres)
Scraping du site https://www.apec.fr
"""
from __future__ import annotations

import re
from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from ..models import JobPosting


def fetch_jobs(query: str, limit: int = 20) -> List[JobPosting]:
    """
    Scrape APEC - offres cadres France.
    
    Note: APEC a une API privée mais pas d'API publique officielle.
    On scrape les résultats de recherche.
    """
    jobs = []
    try:
        # URL de recherche APEC
        url = f"https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles={quote_plus(query)}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        }
        
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            print(f"[APEC] Status {res.status_code}")
            return jobs
        
        soup = BeautifulSoup(res.text, "html.parser")
        
        # APEC structure: chercher les cartes d'offres
        # Sélecteurs à adapter selon structure réelle (change souvent)
        job_cards = soup.select("article.job-card, .result-item, li.offer-item")
        
        if not job_cards:
            # Fallback: chercher tout article ou li avec classe contenant "offer" ou "job"
            job_cards = soup.find_all("article", class_=re.compile(r"(offer|job|result)", re.I))
        
        for idx, card in enumerate(job_cards[:limit]):
            try:
                # Titre
                title_el = card.select_one("h3, .job-title, .offer-title, h2.title")
                title = title_el.get_text(strip=True) if title_el else f"Offre Cadre {idx}"
                
                # Entreprise
                company_el = card.select_one(".company-name, .enterprise, .employer")
                company = company_el.get_text(strip=True) if company_el else "Entreprise"
                
                # Localisation
                location_el = card.select_one(".location, .job-location, .place")
                location = location_el.get_text(strip=True) if location_el else "France"
                city = location.split(",")[0].strip() if location else "Paris"
                
                # Lien
                link_el = card.select_one("a[href*='/offre/']")
                if not link_el:
                    link_el = card.find("a", href=True)
                
                href = link_el.get("href", "") if link_el else ""
                apply_url = f"https://www.apec.fr{href}" if href.startswith("/") else href or "https://www.apec.fr"
                
                # ID unique depuis URL
                job_id = f"apec-{idx}"
                if "numIdOffre=" in href:
                    match = re.search(r"numIdOffre=(\d+)", href)
                    if match:
                        job_id = f"apec-{match.group(1)}"
                
                # Description courte (si présente)
                desc_el = card.select_one(".description, .job-description, p")
                description = desc_el.get_text(strip=True)[:200] if desc_el else f"{title} chez {company}"
                
                # Parser salaire (APEC affiche souvent des fourchettes)
                salary_text = card.get_text()
                salary_min, salary_max = _extract_salary_apec(salary_text)
                
                # Type de contrat (CDI majoritaire sur APEC)
                contract_type = "CDI"
                if "CDD" in salary_text.upper():
                    contract_type = "CDD"
                elif "FREELANCE" in salary_text.upper() or "INDÉPENDANT" in salary_text.upper():
                    contract_type = "Freelance"
                
                # Remote
                remote_type = "onsite"
                text_lower = card.get_text().lower()
                if "télétravail" in text_lower or "remote" in text_lower or "100% télétravail" in text_lower:
                    remote_type = "remote"
                elif "hybride" in text_lower or "partiel" in text_lower:
                    remote_type = "hybrid"
                
                jobs.append(
                    JobPosting(
                        id=job_id,
                        source="apec",
                        source_job_id=job_id,
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
                print(f"[APEC] Error parsing card {idx}: {e}")
                continue
        
        print(f"[APEC] Scraped {len(jobs)} jobs")
    
    except Exception as e:
        print(f"[APEC] Global error: {e}")
    
    return jobs


def _extract_salary_apec(text: str) -> tuple[int | None, int | None]:
    """
    Parse salaire depuis texte APEC.
    Formats typiques: "40K€-55K€", "50 000 € à 70 000 €", "entre 45k et 60k"
    """
    # Pattern 1: 40K-55K ou 40k-55k
    match = re.search(r"(\d+)\s*k[€]?\s*[-–à]\s*(\d+)\s*k", text, re.IGNORECASE)
    if match:
        return (int(match.group(1)) * 1000, int(match.group(2)) * 1000)
    
    # Pattern 2: 40 000 € à 55 000 €
    match = re.search(r"(\d+)\s*000\s*€?\s*[-–à]\s*(\d+)\s*000", text)
    if match:
        return (int(match.group(1)) * 1000, int(match.group(2)) * 1000)
    
    # Pattern 3: entre 45 et 60 (K€ implicite sur APEC)
    match = re.search(r"entre\s+(\d+)\s+et\s+(\d+)", text, re.IGNORECASE)
    if match:
        low = int(match.group(1))
        high = int(match.group(2))
        # Si < 200, probablement en K€
        if low < 200:
            return (low * 1000, high * 1000)
        return (low, high)
    
    return (None, None)


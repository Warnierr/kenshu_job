# 🌐 Sources de Scraping - Sites d'Emploi IT

Liste des sites d'emploi tech qui peuvent être scrapés (en respectant robots.txt et CGU).

## ✅ Actuellement Implémentés

### 🇫🇷 Welcome to the Jungle
- **URL** : https://www.welcometothejungle.com
- **Couverture** : France principalement, quelques offres Europe
- **Spécialité** : Startups, scale-ups, tech
- **Format** : scraping HTML
- **Fichier** : `backend/app/connectors/scraper.py::_scrape_wttj()`

### 🌍 Remotive.io
- **URL** : https://remotive.io
- **Couverture** : International (remote only)
- **Spécialité** : Jobs 100% remote
- **Format** : scraping HTML
- **Fichier** : `backend/app/connectors/scraper.py::_scrape_remotive()`

### 🇫🇷 APEC (Nouveau ✨)
- **URL** : https://www.apec.fr
- **Couverture** : France
- **Spécialité** : Cadres, management, tech seniors
- **Format** : scraping HTML
- **Fichier** : `backend/app/connectors/apec.py`
- **Extraction salaire** : Patterns avancés (40K-55K, "entre 45 et 60", etc.)

### 🌍 Indeed (Nouveau ✨)
- **URL** : https://fr.indeed.com
- **Couverture** : France + international (multi-pays)
- **Spécialité** : Agrégateur généraliste (toutes catégories)
- **Format** : scraping HTML avec headers réalistes
- **Fichier** : `backend/app/connectors/indeed.py`
- **Rate limiting** : Délai 1s entre requêtes
- **Note** : Protections anti-bot, surveiller blocages éventuels

## 🔜 À Implémenter (Facile)

### 🇫🇷 France

#### JobTeaser
- **URL** : https://www.jobteaser.com/fr
- **Couverture** : France, jeunes diplômés, stages
- **Difficulté** : Moyenne (structure React/Next)

#### LesJeudis
- **URL** : https://www.lesjeudis.com
- **Couverture** : France, IT/Digital
- **Difficulté** : Facile (HTML classique)

#### Free-Work
- **URL** : https://www.free-work.com
- **Couverture** : France, missions freelance IT
- **Difficulté** : Facile

#### Chooseyourboss
- **URL** : https://www.chooseyourboss.com
- **Couverture** : France, tech
- **Difficulté** : Moyenne

### 🇪🇺 Europe

#### Landing.jobs
- **URL** : https://landing.jobs
- **Couverture** : Europe (Portugal, Allemagne, UK)
- **Difficulté** : Moyenne

#### Honeypot
- **URL** : https://www.honeypot.io
- **Couverture** : Europe (Allemagne, Pays-Bas)
- **Difficulté** : Difficile (SPA React)

#### StepStone (DE)
- **URL** : https://www.stepstone.de
- **Couverture** : Allemagne, Autriche, Suisse
- **Difficulté** : Moyenne

### 🌍 International

#### We Work Remotely
- **URL** : https://weworkremotely.com
- **Couverture** : Monde entier (remote)
- **Difficulté** : Facile

#### Remote OK
- **URL** : https://remoteok.com
- **Couverture** : Monde entier (remote)
- **Difficulté** : Facile (HTML simple)

#### AngelList (Wellfound)
- **URL** : https://wellfound.com
- **Couverture** : USA, startups
- **Difficulté** : Difficile (GraphQL API)

#### Stack Overflow Jobs
- **URL** : https://stackoverflow.com/jobs
- **Note** : Fermé en 2022, remplacé par intégrations
- **Alternative** : Voir Indeed

#### HackerNews "Who is hiring?"
- **URL** : https://news.ycombinator.com/item?id=whoishiring
- **Couverture** : Startups YC + tech global
- **Difficulté** : Facile (parsing texte)
- **Format** : Thread mensuel

#### LinkedIn Jobs
- **URL** : https://www.linkedin.com/jobs
- **Difficulté** : Très difficile (auth requise, rate limiting)
- **Alternative** : Utiliser API officielle (payante)

#### Indeed
- **URL** : https://www.indeed.com
- **Couverture** : Mondial
- **Difficulté** : Moyenne-Difficile (protection anti-bot)

## 🔑 Avec APIs Officielles (Préférable)

### France Travail (ex-Pôle Emploi)
- **API** : https://api.francetravail.io
- **Clé** : Gratuite après inscription
- **Quota** : Généreux
- **Status** : Stub implémenté, à activer

### Adzuna
- **API** : https://developer.adzuna.com
- **Clé** : Gratuite (limites)
- **Couverture** : Multi-pays (FR, UK, DE, US...)
- **Status** : Stub implémenté, à activer

### EURES (EU)
- **API** : Via partenaires
- **Couverture** : Union Européenne
- **Status** : Stub implémenté

### GitHub Jobs
- **Status** : ❌ Fermé en 2021

### The Muse
- **API** : https://www.themuse.com/developers/api/v2
- **Couverture** : USA principalement
- **Status** : À implémenter

## 📋 Template pour Ajouter un Nouveau Site

```python
def _scrape_nouveau_site(query: str) -> List[JobPosting]:
    """
    Scrape [Nom du Site] - [description courte]
    """
    jobs = []
    try:
        # 1. Construire l'URL de recherche
        url = f"https://example.com/jobs?q={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        # 2. Requête HTTP
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return jobs
        
        # 3. Parser HTML
        soup = BeautifulSoup(res.text, "html.parser")
        job_cards = soup.select(".job-listing")  # Adapter sélecteur
        
        # 4. Extraire données
        for idx, card in enumerate(job_cards[:20]):
            title = card.select_one(".title").get_text(strip=True)
            company = card.select_one(".company").get_text(strip=True)
            location = card.select_one(".location").get_text(strip=True)
            link = card.select_one("a")["href"]
            
            # 5. Parser infos supplémentaires (remote, salaire...)
            remote_type = "hybrid"  # ou parser depuis texte
            salary_min, salary_max = _extract_salary(card.get_text())
            
            # 6. Créer JobPosting
            jobs.append(
                JobPosting(
                    id=f"nouveausite-{idx}",
                    source="nouveausite",
                    source_job_id=f"nouveausite-{idx}",
                    title=title,
                    company=company,
                    country="fr",  # ou parser
                    city=location,
                    remote_type=remote_type,
                    contract_type="CDI",
                    salary_min=salary_min,
                    salary_max=salary_max,
                    currency="EUR" if salary_min else None,
                    apply_url=link,
                    description=f"{title} @ {company}",
                )
            )
    except Exception as e:
        print(f"[scrape error] {e}")
    
    return jobs
```

Puis ajouter dans `fetch_scraping()` :

```python
def fetch_scraping(query: str, country: str = "fr") -> List[JobPosting]:
    jobs: List[JobPosting] = []
    
    if country == "fr":
        jobs.extend(_scrape_wttj(query))
        jobs.extend(_scrape_nouveau_site(query))  # ✅ Ajouter ici
    
    jobs.extend(_scrape_remotive(query))
    return jobs
```

## ⚠️ Considérations Légales

1. **Respecter robots.txt** : vérifier que `/jobs` est autorisé
2. **Rate limiting** : ajouter délais entre requêtes (1-2s)
3. **User-Agent** : identifier votre bot de manière transparente
4. **CGU** : lire conditions d'utilisation du site
5. **Cache** : éviter requêtes répétées (stockage temporaire)
6. **Fallback** : ne pas bloquer si un site échoue

## 🛠️ Outils Avancés

### JobSpy (Python lib)
- **GitHub** : https://github.com/cullenwatson/JobSpy
- **Couverture** : Indeed, LinkedIn, Glassdoor, ZipRecruiter
- **Installation** : `pip install python-jobspy`
- **Usage** :
```python
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "glassdoor"],
    search_term="software engineer",
    location="Paris, France",
    results_wanted=50,
)
```

### Playwright/Selenium
Pour sites avec JavaScript lourd (React/Vue SPAs) :

```python
from playwright.sync_api import sync_playwright

def scrape_with_playwright(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(".job-card")
        content = page.content()
        browser.close()
        return content
```

## 📊 Priorisation Recommandée

1. **APIs officielles** : France Travail, Adzuna (fiables, quotas)
2. **Scraping facile** : Remotive, We Work Remotely (HTML simple)
3. **Scraping moyen** : Welcome to the Jungle, Landing.jobs
4. **Scraping avancé** : LinkedIn, Indeed (anti-bot)
5. **JobSpy** : solution packagée mais dépendance externe

---

**💡 Conseil** : Commencez par 3-4 sources fiables et élargissez progressivement. Privilégiez toujours les APIs officielles quand disponibles.


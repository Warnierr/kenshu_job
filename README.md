# ⚡ DevJobs Hunter - Moteur de Recherche d'Emploi IT

Un moteur de recherche d'emploi cyberpunk pour les développeurs et professionnels de l'IT. Interface néon/hacker style Tron + agrégation multi-sources (APIs + scraping).

## 🎨 Design

- **Thème cyberpunk** : grille animée Tron, néons cyan/rose/violet, typographie Orbitron
- **Catégories IT complètes** : Frontend, Backend, Fullstack, DevOps, Data, ML/AI, Security, etc.
- **UI responsive** : formulaire avancé + cards d'offres interactives avec score de matching

## 🚀 Stack Technique

### Backend
- **FastAPI** : API REST moderne et rapide
- **Pydantic** : validation de données
- **Connecteurs multi-sources** :
  - France Travail API (stub)
  - Adzuna API (stub)
  - EURES API (stub)
  - **Scraping actif** : Welcome to the Jungle, Remotive.io, **APEC**, **Indeed**
- **Scrapeur hebdomadaire** : alimentation automatique BDD
- **Déduplication** : hash + similarité textuelle
- **Scoring CV** : matching keywords + contraintes (remote/contrat/salaire/pays)

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **CSS custom** : animations, effets néon, grid Tron
- **Fonts** : Orbitron (titres), Roboto Mono (texte)

## 📦 Installation

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Le frontend sera accessible sur http://localhost:3000 (ou 3001 si 3000 occupé).

## 🔧 Configuration

### Variables d'environnement (optionnel)

Backend `.env` :
```bash
# APIs (stubs par défaut, scraping actif)
FRANCE_TRAVAIL_API_KEY=your_key
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key
EURES_API_KEY=your_key

# LLM enrichissement (optionnel)
OPENROUTER_API_KEY=your_key

# Base de données (futur)
DATABASE_URL=postgresql://user:pass@localhost:5432/jobs
```

Frontend `.env.local` :
```bash
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

## 🎯 Fonctionnalités

### Mode Sans API (Scraping)
Par défaut, le moteur fonctionne **sans clés API** grâce au scraping :
- **Welcome to the Jungle** (France) : offres tech françaises
- **Remotive.io** (International) : jobs remote IT
- **APEC** (France) : offres cadres
- **Indeed** (Multi-pays) : agrégateur global

Les scrapers sont configurés dans `backend/app/connectors/` avec gestion d'erreurs robuste.

### Scraping Hebdomadaire Automatique 🕐

Un système de scraping périodique alimente la BDD automatiquement :

```bash
# Test manuel
cd backend
python run_weekly_scraper.py
```

**Automatisation** : voir [WEEKLY_SCRAPER.md](WEEKLY_SCRAPER.md) pour configurer Windows Task Scheduler ou cron Linux/Mac.

Avantages :
- ✅ Recherche utilisateur ultra-rapide (lecture BDD)
- ✅ Historique des offres
- ✅ Pas de surcharge des sites externes
- ✅ 20+ requêtes prédéfinies (python, react, devops, data, etc.)

### Catégories IT Disponibles
- Frontend Dev, Backend Dev, Fullstack Dev
- Mobile Dev (iOS/Android/React Native)
- DevOps/SRE, Cloud Architect
- Data Engineer, Data Scientist, ML Engineer, AI Researcher
- QA/Test Engineer, Security Engineer
- Blockchain Dev, Game Dev, Embedded/IoT
- Tech Lead, Engineering Manager, Product Manager
- UI/UX Designer, Solutions Architect

### Filtres Recherche
- **Mots-clés** : python, react, kubernetes, etc.
- **Catégories** : sélection multiple
- **Pays** : codes ISO (fr, de, us, etc.)
- **Contrat** : CDI, CDD, Freelance, Stage
- **Remote** : full remote, hybride, sur site
- **Salaire min** : en €/an
- **Profil CV** : résumé compétences pour scoring

### Pipeline de Données
1. **Ingestion** : appel APIs + scraping parallèle
2. **Normalisation** : schéma `JobPosting` unifié
3. **Déduplication** : hash (source+titre+entreprise+ville)
4. **Scoring** : 
   - Base 50 + bonus keywords présents dans CV
   - Pénalités si contraintes non respectées (remote/contrat/pays/salaire)
5. **Ranking** : tri décroissant par score
6. **Restitution** : JSON + explications (reasons)

## 🛠️ Développement

### Ajouter un nouveau connecteur scraping

Éditer `backend/app/connectors/scraper.py` :

```python
def _scrape_nouveau_site(query: str) -> List[JobPosting]:
    jobs = []
    try:
        url = f"https://example.com/jobs?q={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Parser les offres
        for card in soup.select(".job-card"):
            title = card.select_one(".title").get_text(strip=True)
            company = card.select_one(".company").get_text(strip=True)
            # ...
            jobs.append(JobPosting(...))
    except Exception as e:
        print(f"[scrape error] {e}")
    return jobs
```

Puis appeler dans `fetch_scraping()`.

### Remplacer stubs par vraies APIs

Éditer `backend/app/connectors/france_travail.py` (ou adzuna/eures) :

```python
def fetch_jobs(query: str, limit: int = 20) -> List[JobPosting]:
    # Remplacer mock par vrais appels
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {"Authorization": f"Bearer {FRANCE_TRAVAIL_API_KEY}"}
    params = {"motsCles": query, "range": f"0-{limit}"}
    res = requests.get(url, headers=headers, params=params)
    data = res.json()
    # Parser et mapper vers JobPosting
```

## 📊 Architecture Cible (Future)

- **Postgres + pgvector** : stockage persistant + recherche vectorielle
- **Celery + Redis** : jobs batch récurrents (refresh offres)
- **LLM enrichissement** : extraction salaire/remote/skills via OpenRouter
- **Alertes** : email/webhook/Telegram sur nouvelles offres matchées
- **UI avancée** : filtres sauvegardés, historique candidatures, export CSV/Notion

## 🎨 Personnalisation UI

Les variables CSS sont dans `frontend/app/globals.css` :

```css
:root {
  --neon-cyan: #00f0ff;
  --neon-pink: #ff00ff;
  --neon-purple: #b721ff;
  --neon-green: #39ff14;
  /* ... */
}
```

Modifier couleurs, animations, fonts selon vos préférences.

## 📝 Licence

MIT - Projet éducatif/portfolio. Respectez les CGU des sites scrapés.

## 📚 Documentation Complète

- **[QUICKSTART.md](QUICKSTART.md)** : Démarrage rapide en 3 étapes
- **[WEEKLY_SCRAPER.md](WEEKLY_SCRAPER.md)** : Configuration scraping automatique hebdomadaire
- **[IT_CATEGORIES.md](IT_CATEGORIES.md)** : Liste exhaustive des 50+ rôles IT disponibles
- **[SCRAPING_SOURCES.md](SCRAPING_SOURCES.md)** : Sites scrapables + templates code

## 🧪 Tests

Tester tous les connecteurs :

```bash
cd backend
python test_scraper.py
```

Résultat attendu :
```
✅ France Travail (stub)
✅ Adzuna (stub)
✅ EURES (stub)
✅ Scraping (WTTJ + Remotive)
✅ APEC
✅ Indeed

Success: 6/6
🎉 All connectors working! 🎉
```

## 🤝 Contribution

1. Fork le repo
2. Créer une branche feature (`git checkout -b feat/new-connector`)
3. Commit (`git commit -m 'Add new connector'`)
4. Push (`git push origin feat/new-connector`)
5. Ouvrir une Pull Request

---

**Bon hunt ! 🚀⚡**

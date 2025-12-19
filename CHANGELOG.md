# 📝 Changelog

## [1.1.0] - 2024-12-19 - Scraping Hebdomadaire + APEC + Indeed

### ✨ Nouveautés Majeures

#### 🕐 Système de Scraping Hebdomadaire
- **Scrapeur automatique** pour alimenter la BDD chaque semaine
- **20+ requêtes prédéfinies** : python, react, devops, data, ML, security, etc.
- **Script standalone** : `backend/run_weekly_scraper.py`
- **Documentation complète** : [WEEKLY_SCRAPER.md](WEEKLY_SCRAPER.md)
- **Support Windows Task Scheduler** et cron Linux/Mac
- **Monitoring** : logs, statistiques, alertes email

#### 🆕 Nouveaux Connecteurs

**APEC (Cadres France)**
- Scraping du site https://www.apec.fr
- Spécialité : postes cadres, management, seniors
- Extraction salaire avancée (patterns multiples)
- Détection remote/hybride
- Fichier : `backend/app/connectors/apec.py`

**Indeed (Multi-pays)**
- Scraping du site https://fr.indeed.com
- Couverture : France + international
- Headers réalistes anti-blocage
- Rate limiting respecté (1s délai)
- Extraction salaire (annuel, horaire)
- Fichier : `backend/app/connectors/indeed.py`

### 🔧 Améliorations

#### Pipeline d'Ingestion
- **6 sources actives** : FT (stub), Adzuna (stub), EURES (stub), WTTJ, Remotive, APEC, Indeed
- **Orchestration intelligente** : APEC uniquement pour France, Indeed multi-pays
- **Gestion erreurs robuste** : chaque source isolée (try/except)

#### Documentation
- **4 guides complets** :
  - [README.md](README.md) : vue d'ensemble
  - [QUICKSTART.md](QUICKSTART.md) : démarrage 3 étapes
  - [WEEKLY_SCRAPER.md](WEEKLY_SCRAPER.md) : scraping automatique
  - [IT_CATEGORIES.md](IT_CATEGORIES.md) : 50+ rôles IT
  - [SCRAPING_SOURCES.md](SCRAPING_SOURCES.md) : sites + templates
- **Script de test** : `backend/test_scraper.py` pour valider tous les connecteurs

#### UI/UX
- Design cyberpunk maintenu
- Formulaire avec catégories IT enrichies
- Performance optimisée

### 🐛 Corrections
- Clean restart des serveurs
- Gestion propre des processus backend
- Logs améliorés pour debugging

### 📊 Statistiques
- **Sources totales** : 6 (3 stubs + 3 scraping actif)
- **Catégories IT** : 20+
- **Requêtes hebdo** : 20+ configurables
- **Offres potentielles/semaine** : 500-1000 (selon config)

---

## [1.0.0] - 2024-12-19 - Version Initiale

### ✨ Fonctionnalités
- Interface cyberpunk (néons, Tron grid, Orbitron)
- Backend FastAPI avec pipeline ingestion/scoring
- Frontend Next.js avec formulaire avancé
- 3 connecteurs scraping : WTTJ, Remotive
- 3 API stubs : France Travail, Adzuna, EURES
- Déduplication et scoring CV
- 20 catégories IT

### 🎨 Design
- Thème néon hacker (cyan, rose, violet, vert)
- Animations CSS (glow, hover, grid)
- Responsive design
- Badges interactifs

### 🏗️ Architecture
- Backend : FastAPI + Pydantic
- Frontend : Next.js 14 (App Router) + TypeScript
- Stockage : in-memory (avec hooks BDD)
- Scraping : requests + BeautifulSoup

---

## Roadmap Future

### [1.2.0] - Q1 2025
- [ ] **Postgres + pgvector** : stockage persistant + recherche vectorielle
- [ ] **LLM enrichissement** : extraction automatique salaire/skills
- [ ] **Alertes** : email/Telegram sur nouvelles offres matchées
- [ ] **Historique** : tracking apparition/disparition offres
- [ ] **Export** : CSV/PDF des shortlists

### [1.3.0] - Q2 2025
- [ ] **APIs réelles** : France Travail, Adzuna, EURES avec vraies clés
- [ ] **JobSpy integration** : scraping Indeed/LinkedIn/Glassdoor via lib
- [ ] **Proxy rotation** : pour contourner rate limits
- [ ] **Dashboard admin** : stats scraping, health checks
- [ ] **Multi-utilisateurs** : comptes, profils sauvegardés

### [2.0.0] - Q3 2025
- [ ] **Mobile app** : React Native
- [ ] **Recommandations ML** : suggestions offres basées historique
- [ ] **Salary insights** : tendances salaires par techno/région
- [ ] **Company reviews** : intégration Glassdoor/Trustpilot
- [ ] **Application tracking** : suivi candidatures

---

**Note** : Ce changelog suit le format [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/) et [Semantic Versioning](https://semver.org/lang/fr/).


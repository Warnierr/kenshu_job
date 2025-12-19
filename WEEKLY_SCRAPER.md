# 🕐 Scrapeur Hebdomadaire Automatique

Système de scraping périodique pour alimenter la base de données avec des offres fraîches.

## 🎯 Objectif

Au lieu de scraper à chaque recherche utilisateur, le scrapeur hebdomadaire :
1. **Tourne automatiquement** chaque semaine (dimanche minuit par défaut)
2. **Scrape 20+ requêtes prédéfinies** (python, react, devops, data, etc.)
3. **Agrège toutes les sources** : France Travail, Adzuna, EURES, APEC, Indeed, WTTJ, Remotive
4. **Déduplique et stocke** en BDD
5. **Enrichit** les données (salaire, remote, skills)

✅ **Avantages** :
- Recherche utilisateur ultra-rapide (lecture BDD)
- Historique des offres
- Détection offres retirées
- Moins de charge sur les sites externes
- Respect rate limits

## 📋 Sources Scrapées

### APIs (stubs ou actives)
- ✅ **France Travail API** (stub)
- ✅ **Adzuna API** (stub)
- ✅ **EURES API** (stub)

### Scraping Actif
- ✅ **Welcome to the Jungle** (France, startups)
- ✅ **Remotive.io** (International remote)
- ✅ **APEC** (Cadres France) - **NOUVEAU**
- ✅ **Indeed** (Multi-pays) - **NOUVEAU**

## 🚀 Installation

### 1. Script prêt à l'emploi

Le script est déjà créé : `backend/run_weekly_scraper.py`

### 2. Test manuel

```bash
cd backend
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

python run_weekly_scraper.py
```

Vous verrez :
```
============================================================
WEEKLY JOB SCRAPER
============================================================
[WeeklyScraper] Starting at 2024-12-19 01:30:00
[WeeklyScraper] Scraping: python developer (fr)
  [APEC] Scraped 12 jobs
  [Indeed] Scraped 15 jobs
  → 45 scraped, 38 unique
[WeeklyScraper] Scraping: javascript react (fr)
  ...
[WeeklyScraper] Finished!
  - Total scraped: 876
  - Total stored: 623
  - Errors: 2

============================================================
SUMMARY
============================================================
✅ Scraped: 876 jobs
✅ Stored: 623 unique jobs
✅ No critical errors!
============================================================
```

## ⏰ Automatisation Windows (Task Scheduler)

### Créer la tâche planifiée

1. **Ouvrir Planificateur de tâches** :
   - Win+R → `taskschd.msc`

2. **Créer une tâche de base** :
   - Nom : `DevJobs Weekly Scraper`
   - Déclencheur : **Hebdomadaire** → Dimanche à 00:00
   - Action : **Démarrer un programme**

3. **Programme/script** :
   ```
   C:\Users\User\Desktop\Projets\Kenshu Job\backend\.venv\Scripts\python.exe
   ```

4. **Ajouter des arguments** :
   ```
   run_weekly_scraper.py
   ```

5. **Commencer dans** :
   ```
   C:\Users\User\Desktop\Projets\Kenshu Job\backend
   ```

6. **Options avancées** :
   - ☑ Exécuter même si l'utilisateur n'est pas connecté
   - ☑ Exécuter avec les autorisations maximales
   - ☐ Ne démarrer que si l'ordinateur est branché (décocher pour laptop)

7. **Sauvegarder** et tester :
   - Clic droit sur la tâche → **Exécuter**

### PowerShell one-liner (alternative)

```powershell
$action = New-ScheduledTaskAction -Execute "C:\Users\User\Desktop\Projets\Kenshu Job\backend\.venv\Scripts\python.exe" -Argument "run_weekly_scraper.py" -WorkingDirectory "C:\Users\User\Desktop\Projets\Kenshu Job\backend"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 00:00
Register-ScheduledTask -TaskName "DevJobs Weekly Scraper" -Action $action -Trigger $trigger -Description "Scraping hebdomadaire offres IT"
```

## 🐧 Automatisation Linux/Mac (cron)

Éditer crontab :
```bash
crontab -e
```

Ajouter :
```cron
# Chaque dimanche à 00:00
0 0 * * 0 cd /path/to/backend && .venv/bin/python run_weekly_scraper.py >> /var/log/weekly_scraper.log 2>&1
```

Ou avec `anacron` pour exécution différée si machine éteinte.

## 📊 Configuration Requêtes

Éditer `backend/app/scheduler/weekly_scraper.py` :

```python
WEEKLY_QUERIES = [
    {"keywords": "python developer", "countries": ["fr"]},
    {"keywords": "javascript react", "countries": ["fr"]},
    # ... ajouter vos requêtes
    {"keywords": "votre technologie", "countries": ["fr", "de"]},
]
```

### Exemples de requêtes utiles

```python
# Langages
{"keywords": "python django", "countries": ["fr"]},
{"keywords": "javascript typescript", "countries": ["fr"]},
{"keywords": "java spring boot", "countries": ["fr"]},
{"keywords": "c# dotnet", "countries": ["fr"]},
{"keywords": "php laravel", "countries": ["fr"]},
{"keywords": "ruby rails", "countries": ["fr"]},

# Frameworks frontend
{"keywords": "react nextjs", "countries": ["fr"]},
{"keywords": "vue nuxt", "countries": ["fr"]},
{"keywords": "angular", "countries": ["fr"]},
{"keywords": "svelte", "countries": ["fr"]},

# Mobile
{"keywords": "ios swift swiftui", "countries": ["fr"]},
{"keywords": "android kotlin jetpack", "countries": ["fr"]},
{"keywords": "react native", "countries": ["fr"]},
{"keywords": "flutter", "countries": ["fr"]},

# DevOps/Cloud
{"keywords": "kubernetes docker", "countries": ["fr", "de"]},
{"keywords": "aws architect", "countries": ["fr"]},
{"keywords": "azure devops", "countries": ["fr"]},
{"keywords": "terraform ansible", "countries": ["fr"]},
{"keywords": "gitlab ci jenkins", "countries": ["fr"]},

# Data/AI
{"keywords": "data engineer spark", "countries": ["fr"]},
{"keywords": "data scientist", "countries": ["fr"]},
{"keywords": "machine learning", "countries": ["fr", "us"]},
{"keywords": "mlops", "countries": ["fr"]},
{"keywords": "nlp transformers", "countries": ["fr", "us"]},

# Sécurité
{"keywords": "security engineer pentest", "countries": ["fr"]},
{"keywords": "devsecops", "countries": ["fr"]},
{"keywords": "soc analyst", "countries": ["fr"]},

# Autres
{"keywords": "blockchain solidity", "countries": ["fr", "de"]},
{"keywords": "game developer unity", "countries": ["fr"]},
{"keywords": "embedded iot", "countries": ["fr"]},
```

## 🔧 Monitoring & Logs

### Logs simples

Rediriger stdout vers fichier :

**Windows** (Task Scheduler) :
- Programme : `cmd.exe`
- Arguments : `/c "C:\...\python.exe run_weekly_scraper.py > logs\scraper.log 2>&1"`

**Linux/Mac** :
```bash
0 0 * * 0 cd /path/to/backend && .venv/bin/python run_weekly_scraper.py >> /var/log/weekly_scraper.log 2>&1
```

### Logs rotatifs (recommandé)

Installer `logrotate` ou équivalent Windows pour éviter logs géants.

### Alertes email

Modifier `run_weekly_scraper.py` pour envoyer email si erreurs :

```python
import smtplib
from email.message import EmailMessage

if result['errors']:
    msg = EmailMessage()
    msg['Subject'] = '⚠️ Weekly Scraper Errors'
    msg['From'] = 'scraper@yourapp.com'
    msg['To'] = 'admin@yourapp.com'
    msg.set_content(f"Errors:\n" + "\n".join(result['errors']))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('user', 'pass')
        smtp.send_message(msg)
```

## 📈 Statistiques

Après plusieurs semaines, vous aurez :
- **Plusieurs milliers d'offres** en BDD
- **Historique** des postes (date apparition/disparition)
- **Tendances salaires** par techno/région
- **Détection entreprises** qui recrutent activement

## 🎯 Next Steps

### 1. Base de Données Persistante

Remplacer `MemoryStore` par Postgres :

```python
# backend/app/storage/postgres.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)

def upsert_jobs(jobs):
    session = Session()
    for job in jobs:
        session.merge(job)  # INSERT or UPDATE
    session.commit()
```

### 2. Historisation

Ajouter champs `first_seen`, `last_seen`, `is_active` :

```python
class JobPosting(BaseModel):
    # ... champs existants
    first_seen: datetime
    last_seen: datetime
    is_active: bool = True
```

### 3. Enrichissement LLM

Après stockage, lancer enrichissement :

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

for job in new_jobs:
    if not job.salary_min:
        # Extraire salaire depuis description
        prompt = f"Extract salary range from: {job.description}"
        response = client.chat.completions.create(...)
        job.salary_min, job.salary_max = parse_llm_response(response)
```

### 4. Notifications Utilisateurs

Si un utilisateur a sauvegardé des critères, l'alerter sur nouvelles offres matchées :

```python
for user in users_with_alerts:
    matching_jobs = [j for j in new_jobs if matches_user_criteria(j, user)]
    if matching_jobs:
        send_email_alert(user, matching_jobs)
```

## ⚠️ Considérations Importantes

### Rate Limiting
- **Délais entre requêtes** : 1-2 secondes (déjà dans Indeed connector)
- **Rotation IP** : si volume important (proxies)
- **Headers réalistes** : User-Agent, Accept, etc.

### Respect CGU
- ✅ APEC : pas de robots.txt bloquant `/recherche-emploi`
- ✅ Indeed : rate limiting respecté
- ✅ WTTJ : parsing HTML public
- ✅ Remotive : API publique

### Fallback
Le scraper ne doit **jamais bloquer** l'application principale :
- Chaque source est dans un `try/except`
- Erreurs loggées mais non critiques
- Pipeline continue même si 1-2 sources échouent

---

**🎯 Résultat** : Votre BDD se remplit automatiquement chaque semaine avec des centaines d'offres IT fraîches, prêtes à être matchées instantanément avec vos utilisateurs ! 🚀


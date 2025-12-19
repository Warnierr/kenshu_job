# 🚀 Guide de Démarrage Rapide

## ⚡ Lancement en 3 étapes

### 1. Backend (Terminal 1)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ Backend prêt sur http://localhost:8000

### 2. Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend prêt sur http://localhost:3000

### 3. Utilisation

1. Ouvrir http://localhost:3000 dans votre navigateur
2. Sélectionner vos **catégories IT** (Backend Dev, DevOps, Data, etc.)
3. Ajouter vos **mots-clés tech** (python, react, kubernetes...)
4. Configurer vos **critères** :
   - Pays (fr, de, us...)
   - Type contrat (CDI, Freelance...)
   - Remote (full remote, hybride, sur site)
   - Salaire minimum
   - Résumé de votre CV/profil
5. Cliquer sur **🚀 LANCER SCAN**
6. Les offres apparaissent avec leur **score de matching** ⚡

## 🎨 Design Cyberpunk

- **Grille animée Tron** en arrière-plan
- **Néons cyan/rose/violet** sur tous les éléments
- **Typographie Orbitron** pour les titres
- **Effets hover** avec glow et animations

## 🔧 Mode Sans API (Scraping Actif)

Par défaut, l'application fonctionne **sans clés API** grâce au scraping :

✅ **Welcome to the Jungle** (France)
✅ **Remotive.io** (International remote)
✅ **APEC** (Cadres France)
✅ **Indeed** (Multi-pays)

Les stubs France Travail/Adzuna/EURES sont présents mais renvoient des données de test.

## 🕐 Scraping Hebdomadaire (Bonus)

Pour alimenter automatiquement votre BDD chaque semaine :

```bash
cd backend
python run_weekly_scraper.py
```

Configuration complète : voir [WEEKLY_SCRAPER.md](WEEKLY_SCRAPER.md)

## 📊 Scoring des Offres

Le score (sur 100) est calculé ainsi :

- **Base** : 50 points
- **+5 points** par mot-clé de votre CV présent dans l'offre
- **-20 points** si remote ne correspond pas
- **-15 points** si type de contrat ne correspond pas
- **-10 points** si pays ne correspond pas
- **-10 points** si salaire < votre minimum

## 🎯 Catégories IT Disponibles

- Frontend Dev, Backend Dev, Fullstack Dev
- Mobile Dev (iOS/Android/RN)
- DevOps/SRE, Cloud Architect
- Data Engineer, Data Scientist
- ML Engineer, AI Researcher
- QA/Test Engineer
- Security Engineer, Blockchain Dev
- Game Dev, Embedded/IoT
- Tech Lead, Engineering Manager
- Product Manager, UI/UX Designer
- Solutions Architect

## 🐛 Dépannage

### Backend ne démarre pas (port 8000 occupé)

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Frontend ne démarre pas (port 3000 occupé)

Next.js essaiera automatiquement le port 3001, 3002, etc.

Ou forcer un port :
```bash
npm run dev -- -p 3005
```

### Erreur module BeautifulSoup

```bash
cd backend
.venv\Scripts\activate
pip install beautifulsoup4 lxml
```

### Offres vides / scraping échoue

C'est normal ! Les scrapers sont basiques et dépendent de la structure HTML des sites :

- **Solution 1** : Activer les APIs réelles (voir README.md)
- **Solution 2** : Améliorer les sélecteurs CSS dans `backend/app/connectors/scraper.py`
- **Solution 3** : Ajouter de nouveaux sites à scraper

## 🚀 Prochaines Étapes

1. **Ajouter vraies clés API** (France Travail, Adzuna, EURES)
2. **Postgres + pgvector** pour stockage persistant
3. **LLM enrichissement** (extraction salaire/skills automatique)
4. **Alertes** email/Telegram sur nouvelles offres
5. **Export CSV/PDF** des shortlists
6. **Historique candidatures**

## 📝 Personnalisation Design

Éditer `frontend/app/globals.css` :

```css
:root {
  --neon-cyan: #00f0ff;    /* Changez en #00ff00 pour vert */
  --neon-pink: #ff00ff;    /* Changez en #ff0066 pour rose vif */
  --neon-purple: #b721ff;  /* Changez en #ffaa00 pour orange */
  /* ... */
}
```

---

**Bon hunt ! 🔥⚡🚀**


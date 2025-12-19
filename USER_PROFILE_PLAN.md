# 👤 Plan : Système de Profil Utilisateur avec CV

## 🎯 Objectif

Permettre aux utilisateurs de :
1. **Créer et sauvegarder un profil** avec leur CV
2. **Entrer leur CV** de 3 façons : texte libre, upload fichier (PDF/DOCX), ou formulaire structuré
3. **Modifier leur profil** à tout moment
4. **Utiliser automatiquement** les données du profil pour améliorer le scoring des offres

## 📋 Fonctionnalités

### 1. Gestion de Profil

#### Backend (FastAPI)

**Nouveau modèle : `UserProfile`**
```python
class UserProfile(BaseModel):
    id: str  # UUID
    user_id: str  # Identifiant utilisateur (email ou UUID)
    created_at: datetime
    updated_at: datetime
    
    # Informations personnelles
    full_name: str | None
    email: str | None
    phone: str | None
    location: str | None  # Ville, Pays
    
    # CV (3 formats possibles)
    cv_text: str | None  # Texte libre
    cv_file_path: str | None  # Chemin vers fichier uploadé
    cv_structured: dict | None  # Données structurées (formulaire)
    
    # Données extraites du CV (pour scoring)
    skills: list[str]  # Compétences techniques
    experience_years: int | None  # Années d'expérience
    experience_level: str | None  # Junior/Mid/Senior
    sectors: list[str]  # Secteurs d'activité
    languages: list[str]  # Langues parlées
    education: list[dict]  # Formation
    
    # Préférences de recherche
    preferred_contract_types: list[str]  # CDI, CDD, Freelance...
    preferred_remote: str | None  # remote, hybrid, onsite
    salary_min: int | None
    preferred_countries: list[str]  # fr, de, us...
    preferred_categories: list[str]  # Backend Dev, DevOps...
```

**Nouveaux endpoints :**
- `POST /api/profile` - Créer un profil
- `GET /api/profile/{user_id}` - Récupérer un profil
- `PUT /api/profile/{user_id}` - Mettre à jour un profil
- `DELETE /api/profile/{user_id}` - Supprimer un profil
- `POST /api/profile/{user_id}/upload-cv` - Upload fichier CV
- `POST /api/profile/{user_id}/parse-cv` - Parser CV (texte ou fichier)

#### Frontend (Next.js)

**Nouvelle page : `/profile`**
- Formulaire de création/édition de profil
- 3 onglets pour les 3 modes d'entrée CV :
  1. **Texte libre** : Textarea pour coller le CV
  2. **Upload fichier** : Drag & drop ou file input (PDF, DOCX)
  3. **Formulaire structuré** : Champs pour expérience, compétences, etc.

**Composants :**
- `ProfileForm.tsx` - Formulaire principal
- `CVTextInput.tsx` - Saisie texte libre
- `CVFileUpload.tsx` - Upload fichier
- `CVStructuredForm.tsx` - Formulaire structuré
- `ProfileView.tsx` - Affichage profil sauvegardé

### 2. Parsing de CV

#### Extraction automatique depuis texte/fichier

**Option 1 : Règles simples (MVP)**
- Regex pour extraire : compétences, années d'expérience, langues
- Patterns : "5 ans", "Python", "Anglais", etc.

**Option 2 : LLM (OpenRouter) - Phase 2**
- Envoyer CV à LLM pour extraction structurée
- Prompt : "Extrait compétences, expérience, formation depuis ce CV"
- Retour : JSON structuré

**Bibliothèques utiles :**
- `python-docx` : Parser DOCX
- `PyPDF2` ou `pdfplumber` : Parser PDF
- `spaCy` ou `NLTK` : NLP pour extraction

### 3. Intégration avec Recherche

**Modification du scoring :**
- Si profil existe → utiliser données profil au lieu de `cv_summary`
- Scoring amélioré avec :
  - Compétences exactes du profil
  - Années d'expérience vs exigences
  - Secteurs d'activité
  - Langues requises

**Endpoint `/search` modifié :**
```python
@app.post("/search")
def search(req: SearchRequest, user_id: str | None = None):
    # Si user_id fourni, charger profil
    profile = None
    if user_id:
        profile = get_user_profile(user_id)
    
    # Utiliser profil pour enrichir recherche
    if profile:
        req.cv_summary = build_cv_summary_from_profile(profile)
        req.skills = profile.skills
        # etc.
    
    jobs = pipeline.search(req)
    return jobs
```

### 4. Stockage

**Phase 1 : Stockage fichier (MVP)**
- JSON files dans `backend/data/profiles/`
- Un fichier par utilisateur : `{user_id}.json`

**Phase 2 : Base de données (Production)**
- Postgres avec table `user_profiles`
- Stockage fichiers CV dans `backend/uploads/cvs/`
- Index sur `user_id` pour recherche rapide

## 🗂️ Structure de Fichiers

```
backend/
├── app/
│   ├── api/
│   │   └── profile.py          # Endpoints profil
│   ├── models/
│   │   └── profile.py          # Modèle UserProfile
│   ├── services/
│   │   ├── cv_parser.py        # Parsing CV (texte/fichier)
│   │   └── profile_service.py  # Logique métier profil
│   └── storage/
│       └── profile_store.py    # Stockage profils
├── uploads/
│   └── cvs/                    # Fichiers CV uploadés
└── data/
    └── profiles/               # JSON profils (MVP)

frontend/
├── app/
│   ├── profile/
│   │   ├── page.tsx            # Page profil
│   │   └── components/
│   │       ├── ProfileForm.tsx
│   │       ├── CVTextInput.tsx
│   │       ├── CVFileUpload.tsx
│   │       └── CVStructuredForm.tsx
│   └── api/
│       └── profile.ts          # Client API profil
```

## 📝 Étapes d'Implémentation

### Phase 1 : MVP (Semaine 1)

**Jour 1-2 : Backend - Modèle et Stockage**
- [ ] Créer modèle `UserProfile` (Pydantic)
- [ ] Créer `ProfileStore` (stockage JSON)
- [ ] Endpoints CRUD basiques

**Jour 3-4 : Backend - Parsing CV**
- [ ] Parser texte simple (regex)
- [ ] Upload fichier (PDF/DOCX)
- [ ] Extraction compétences/expérience basique

**Jour 5 : Frontend - Formulaire**
- [ ] Page `/profile`
- [ ] 3 onglets (texte/upload/formulaire)
- [ ] Intégration API

**Jour 6-7 : Intégration Recherche**
- [ ] Modifier `/search` pour utiliser profil
- [ ] Améliorer scoring avec données profil
- [ ] Tests end-to-end

### Phase 2 : Améliorations (Semaine 2)

- [ ] LLM parsing (OpenRouter) pour extraction avancée
- [ ] Validation CV (format, taille)
- [ ] Prévisualisation CV parsé
- [ ] Export profil (PDF/JSON)
- [ ] Historique modifications

### Phase 3 : Production

- [ ] Migration vers Postgres
- [ ] Stockage fichiers (S3 ou local sécurisé)
- [ ] Authentification utilisateur
- [ ] Multi-profils par utilisateur
- [ ] Partage profil (lien public)

## 🔧 Dépendances à Ajouter

**Backend :**
```txt
python-docx==1.1.0      # Parser DOCX
PyPDF2==3.0.1          # Parser PDF
pdfplumber==0.10.3     # Alternative PDF (meilleur)
spacy==3.7.2           # NLP (optionnel)
```

**Frontend :**
```json
"react-dropzone": "^14.2.3"  // Upload drag & drop
"file-saver": "^2.0.5"       // Téléchargement fichiers
```

## 🎨 UI/UX

### Design Cyberpunk Maintenu
- Formulaire avec bordures néon
- Upload zone avec effet glow au survol
- Prévisualisation CV avec style terminal
- Badges compétences avec couleurs néon

### Workflow Utilisateur
1. **Première visite** : Invitation à créer profil
2. **Création profil** : Choix mode entrée CV
3. **Parsing automatique** : Extraction données
4. **Vérification** : Utilisateur peut corriger données extraites
5. **Sauvegarde** : Profil disponible pour recherches futures
6. **Recherche** : Profil utilisé automatiquement si connecté

## 🔐 Sécurité

- **Validation fichiers** : Type, taille max (10MB), scan antivirus
- **Sanitization** : Nettoyer données utilisateur (XSS)
- **Rate limiting** : Limiter uploads/parsing
- **Authentification** : JWT tokens (Phase 3)

## 📊 Métriques

- Taux de création profil
- Taux d'utilisation profil dans recherches
- Amélioration scoring avec profil vs sans
- Temps parsing CV

---

**🎯 Résultat Final** : Un système complet où l'utilisateur peut sauvegarder son CV une fois, et toutes ses recherches futures utilisent automatiquement ces données pour un matching optimal ! 🚀


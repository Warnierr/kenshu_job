# 🚀 Configuration GitHub

## 📤 Push vers GitHub

### 1. Créer un repository sur GitHub

1. Aller sur https://github.com/new
2. Nom du repo : `kenshu-job` (ou autre nom)
3. **Ne pas** initialiser avec README, .gitignore ou licence (déjà présents)
4. Cliquer sur "Create repository"

### 2. Lier le repo local à GitHub

```bash
# Ajouter le remote (remplacer USERNAME par votre username GitHub)
git remote add origin https://github.com/USERNAME/kenshu-job.git

# Ou avec SSH
git remote add origin git@github.com:USERNAME/kenshu-job.git
```

### 3. Push vers GitHub

```bash
# Renommer la branche en main (si nécessaire)
git branch -M main

# Push initial
git push -u origin main
```

### 4. Vérification

Vérifier que tout est bien pushé :
```bash
git remote -v
git log --oneline
```

## 🔄 Workflow pour les prochains commits

```bash
# 1. Vérifier les changements
git status

# 2. Ajouter les fichiers modifiés
git add .

# 3. Commit avec message descriptif
git commit -m "Description des changements"

# 4. Push vers GitHub
git push
```

## 📝 Exemples de messages de commit

- `feat: Ajout système de profil utilisateur`
- `fix: Correction bug CORS`
- `docs: Mise à jour README`
- `refactor: Optimisation scoring CV`
- `style: Amélioration design cyberpunk`

## 🔐 Authentification GitHub

Si vous utilisez HTTPS et que GitHub demande un token :

1. Aller sur https://github.com/settings/tokens
2. Générer un nouveau token (classic)
3. Permissions : `repo` (accès complet aux repos)
4. Utiliser ce token comme mot de passe lors du push

Ou utiliser SSH (recommandé) :
1. Générer une clé SSH : `ssh-keygen -t ed25519 -C "votre_email@example.com"`
2. Ajouter la clé publique à GitHub : Settings → SSH and GPG keys
3. Utiliser l'URL SSH pour le remote

---

**Note** : Le repo est maintenant prêt à être pushé sur GitHub ! 🎉


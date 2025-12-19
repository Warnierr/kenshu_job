# UI Next.js (MVP)

UI minimale pour interroger le backend FastAPI (endpoints `/ingest` puis `/search`). Par défaut, l'URL backend est `http://localhost:8000` (surchargeable via `NEXT_PUBLIC_API_BASE`).

## Démarrage
```bash
cd frontend
npm install
npm run dev
# http://localhost:3000
```

Le formulaire envoie vos critères (mots-clés, pays, contrat, remote, salaire min, résumé CV) et affiche la shortlist scorée.


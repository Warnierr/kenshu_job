# 🎯 Catégories IT Complètes

Liste exhaustive des rôles disponibles dans le moteur de recherche.

## 💻 Développement

### Frontend Development
- **Frontend Dev** : React, Vue, Angular, Svelte
- **UI Developer** : HTML/CSS/JavaScript avancé
- **Web Designer/Dev** : Design + intégration

### Backend Development
- **Backend Dev** : Python, Node.js, Java, Go, .NET
- **API Developer** : REST, GraphQL, gRPC
- **Microservices Architect**

### Fullstack Development
- **Fullstack Dev** : Frontend + Backend
- **MERN/MEAN Stack** : MongoDB, Express, React/Angular, Node
- **JAMstack Developer** : Next.js, Gatsby, Netlify

### Mobile Development
- **Mobile Dev** : iOS (Swift), Android (Kotlin)
- **React Native Developer**
- **Flutter Developer**
- **Xamarin/.NET MAUI Developer**

## ☁️ Infrastructure & Ops

### DevOps & SRE
- **DevOps Engineer** : CI/CD, automation, monitoring
- **SRE (Site Reliability Engineer)** : haute dispo, performance
- **Platform Engineer** : Kubernetes, Terraform, Ansible

### Cloud
- **Cloud Architect** : AWS, Azure, GCP
- **Cloud Engineer** : Infrastructure as Code
- **Solutions Architect** : conception systèmes distribués

### Sécurité
- **Security Engineer** : pentest, audits, hardening
- **DevSecOps** : sécurité intégrée CI/CD
- **Security Architect** : politique sécurité globale

## 📊 Data & IA

### Data Engineering
- **Data Engineer** : pipelines ETL/ELT, data lakes
- **Big Data Engineer** : Spark, Hadoop, Kafka
- **Analytics Engineer** : dbt, transformation données

### Data Science & IA
- **Data Scientist** : statistiques, ML, visualisation
- **ML Engineer** : MLOps, déploiement modèles
- **AI Researcher** : recherche fondamentale, publications
- **NLP Engineer** : traitement langage naturel
- **Computer Vision Engineer** : reconnaissance image/vidéo

## 🔧 Spécialités

### Quality Assurance
- **QA Engineer** : tests manuels et automatisés
- **Test Automation Engineer** : Selenium, Cypress, Playwright
- **Performance Engineer** : tests charge, optimisation

### Blockchain & Web3
- **Blockchain Developer** : Solidity, smart contracts
- **Web3 Developer** : DApps, DeFi, NFT
- **Crypto Engineer** : protocoles, consensus

### Gaming
- **Game Developer** : Unity, Unreal Engine, Godot
- **Gameplay Programmer** : mécaniques de jeu
- **Game Engine Developer** : moteurs custom

### Systèmes Embarqués
- **Embedded/IoT** : C/C++, firmware, RTOS
- **Firmware Engineer** : microcontrôleurs, drivers
- **Robotics Engineer** : ROS, contrôle robots

## 👔 Management & Produit

### Tech Leadership
- **Tech Lead** : lead technique équipe dev
- **Engineering Manager** : management + stratégie tech
- **CTO / VP Engineering** : direction technique

### Product Management
- **Product Manager** : roadmap produit, specs
- **Technical Product Manager** : PM avec background tech
- **Product Owner** (Scrum/Agile)

### Design
- **UI/UX Designer** : interfaces, expérience utilisateur
- **Product Designer** : design produit end-to-end
- **UX Researcher** : études utilisateurs

## 🏗️ Architecture

### Solutions Architecture
- **Solutions Architect** : conception solutions complexes
- **Enterprise Architect** : architecture SI global
- **Software Architect** : patterns, best practices

## 🎓 Autres Rôles Tech

- **Technical Writer** : documentation technique
- **Developer Advocate** : évangélisation, contenu
- **Sales Engineer / Pre-sales** : support ventes technique
- **Support Engineer** : support technique niveau 2/3
- **System Administrator** : gestion serveurs, infra
- **Database Administrator (DBA)** : gestion BDD
- **Network Engineer** : réseaux, VPN, load balancing

## 📝 Comment Ajouter une Catégorie

Éditer `frontend/app/page.tsx` :

```typescript
const IT_CATEGORIES = [
  "Frontend Dev",
  "Backend Dev",
  // ... existants ...
  "Nouvelle Catégorie",  // Ajouter ici
];
```

La catégorie sera automatiquement intégrée au formulaire et aux keywords de recherche.

## 🔍 Mapping avec Sources

Les catégories sont converties en keywords pour interroger les APIs/scraping :

- **Frontend Dev** → `frontend react vue angular`
- **Data Scientist** → `data scientist python machine learning`
- **DevOps/SRE** → `devops sre kubernetes docker`

Vous pouvez affiner le mapping dans `backend/app/services/pipeline.py` pour optimiser les résultats.

---

**💡 Conseil** : Commencez par sélectionner 2-3 catégories proches de votre profil pour des résultats ciblés, puis élargissez si besoin.


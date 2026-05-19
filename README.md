# SentinelOne API Simulator

Simulateur de l'API de management SentinelOne pour tester et démontrer l'intégration Cortex XSIAM sans avoir accès à un environnement SentinelOne réel.

## Contexte

Ce projet simule le comportement de l'API REST SentinelOne v2.1 pour permettre la démonstration complète de l'intégration **SentinelOne V2** dans Cortex XSIAM. Toutes les réponses sont générées avec des données fictives mais réalistes.

## Endpoints simulés

### Agents (`/web/api/v2.1/agents/...`)
- `GET /agents` — Lister les agents / rechercher
- `GET /agents/processes` — Processus en cours sur un agent
- `GET /agents/applications` — Applications installées
- `POST /agents/actions/connect` — Reconnecter un agent
- `POST /agents/actions/disconnect` — Déconnecter un agent
- `POST /agents/actions/broadcast` — Envoyer un message
- `POST /agents/actions/shutdown` / `uninstall` — Actions sur agents
- `POST /agents/actions/initiate-scan` / `abort-scan` — Scan antivirus
- `POST /agents/actions/fetch-logs` — Récupérer les logs
- `POST /agents/{id}/actions/fetch-files` — Récupérer un fichier
- `GET /agents/{id}/uploads/{activity_id}` — Télécharger le fichier récupéré

### Menaces (`/web/api/v2.1/threats/...`)
- `GET /threats` — Lister les menaces
- `POST /threats/mark-as-threat` / `mark-as-resolved` — Changer l'état
- `POST /threats/mitigate/{action}` — Mitiger (quarantine, kill, remediate...)
- `POST /threats/analyst-verdict` / `incident` — Mettre à jour le verdict/statut
- `GET /threats/{id}/notes` / `POST /threats/notes` — Notes sur une menace
- `GET /threats/{id}/timeline` — Timeline d'une menace
- `POST /threats/fetch-file` / `GET /threats/{id}/download-from-cloud` — Fichier de la menace
- `GET /private/threats/summary` — Résumé des menaces
- `GET /private/threats/{id}/analysis` — Analyse détaillée

### Alertes Cloud Detection (`/web/api/v2.1/cloud-detection/...`)
- `GET /cloud-detection/alerts` — Lister les alertes
- `POST /cloud-detection/alerts/analyst-verdict` / `incident` — Mettre à jour
- `POST /cloud-detection/rules` — Créer une règle STAR
- `GET /cloud-detection/rules` — Lister les règles STAR
- `PUT /cloud-detection/rules/{id}` — Modifier une règle STAR
- `PUT /cloud-detection/rules/enable` / `disable` — Activer/désactiver
- `DELETE /cloud-detection/rules` — Supprimer des règles

### Deep Visibility (`/web/api/v2.1/dv/...`)
- `POST /dv/init-query` — Lancer une requête DV
- `GET /dv/query-status` — État de la requête
- `GET /dv/events` — Résultats des événements
- `GET /dv/events/process` — Résultats des processus
- `POST /dv/events/pq` — Lancer une Power Query
- `GET /dv/events/pq` / `GET /dv/events/pq-ping` — Résultats et statut PQ

### UAM Alerts (`/web/api/v2.1/unifiedalerts/graphql`)
- `POST` GraphQL — Lister les alertes UAM
- `POST` GraphQL mutation — Mettre à jour statut / verdict

### Autres
- `GET /activities` — Journal d'activités
- `GET /sites` / `GET /sites/{id}` / `PUT .../reactivate` — Sites
- `GET /groups` / `DELETE /groups/{id}` / `PUT .../move-agents` — Groupes
- `GET|POST|DELETE /exclusions` — Liste blanche
- `GET|POST|DELETE /restrictions` — Liste noire (blocklist)
- `GET /hashes/{hash}/reputation|verdict|classification` — Réputation hash
- `GET|POST|DELETE /threat-intelligence/iocs` — IOCs
- `GET /accounts` — Comptes
- `POST /remote-scripts/execute` / `GET /remote-scripts/status` — Scripts distants
- `GET /singularity-marketplace/applications` — Marketplace
- `GET /service-users` — Utilisateurs de service

## Installation locale

### Prérequis
- Python 3.11+

### Lancement

```bash
cd simulator
pip install -r requirements.txt
python app.py
```

Le simulateur démarre sur `http://localhost:8080`

### Test rapide

```bash
# Health check
curl http://localhost:8080/health

# Lister les agents
curl -H "Authorization: ApiToken test-api-token-sentinelone" \
  "http://localhost:8080/web/api/v2.1/agents"

# Lister les menaces
curl -H "Authorization: ApiToken test-api-token-sentinelone" \
  "http://localhost:8080/web/api/v2.1/threats"
```

## Configuration dans Cortex XSIAM

1. **Settings → Integrations** → Rechercher **SentinelOne V2**
2. Configurer :
   - **Server URL** : URL du simulateur (ex: `https://sentinelone-simulator-xxx.run.app`)
   - **API Token** : `test-api-token-sentinelone`
   - **API Version** : `2.1`
   - **Trust any certificate** : décoché (HTTPS automatique sur GCP)
3. **Test** → la connexion doit réussir
4. Activer **Fetch incidents** → choisir `Threats` ou `Both`
5. **Save**

## Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `API_TOKEN` | `test-api-token-sentinelone` | Token d'authentification |
| `MIN_ITEMS` | `1` | Nombre minimum d'éléments générés |
| `MAX_ITEMS` | `10` | Nombre maximum d'éléments générés |
| `DEBUG` | `True` | Mode debug Flask |
| `PORT` | `8080` | Port d'écoute |

## Déploiement GCP

📖 **[Guide complet de déploiement GCP → DEPLOYMENT_GCP.md](DEPLOYMENT_GCP.md)**

Le guide couvre :
- Création et configuration du projet GCP
- Déploiement Cloud Run (recommandé)
- Gestion des permissions (y compris les org policies)
- Configuration XSIAM pas à pas
- Dépannage des erreurs courantes

### Déploiement rapide (si gcloud est déjà configuré)

```bash
# Depuis la racine du projet
bash deploy-cloudrun.sh
```

## Structure du projet

```
sentinelone-simul/
├── simulator/
│   ├── app.py                  # Application Flask principale
│   ├── auth.py                 # Authentification ApiToken
│   ├── config.py               # Configuration
│   ├── requirements.txt        # Dépendances Python
│   ├── generators/             # Générateurs de données fictives
│   │   ├── base.py            # Utilitaires communs
│   │   ├── agents.py          # Données agents
│   │   ├── threats.py         # Données menaces
│   │   ├── alerts.py          # Données alertes / UAM
│   │   ├── activities.py      # Journal d'activités
│   │   ├── sites.py           # Sites
│   │   └── groups.py          # Groupes
│   └── routes/                # Endpoints API
│       ├── agents.py          # /agents/*
│       ├── threats.py         # /threats/*
│       ├── alerts.py          # /cloud-detection/alerts/*
│       ├── star.py            # /cloud-detection/rules/*
│       ├── dv.py              # /dv/*
│       ├── uam.py             # /unifiedalerts/graphql
│       ├── iocs.py            # /threat-intelligence/iocs
│       ├── exclusions.py      # /exclusions
│       ├── restrictions.py    # /restrictions
│       ├── hashes.py          # /hashes/*
│       ├── sites.py           # /sites/*
│       ├── groups.py          # /groups/*
│       ├── activities.py      # /activities
│       ├── accounts.py        # /accounts
│       ├── remote_scripts.py  # /remote-scripts/*
│       └── misc.py            # /service-users, /singularity-marketplace, ...
├── deployment/
│   ├── Dockerfile             # Image Docker (Python 3.11 slim)
│   └── app.yaml               # Config Cloud Run / App Engine
├── cloudbuild.yaml            # Pipeline de build GCP
├── deploy-cloudrun.sh         # Script de déploiement automatisé
└── README.md
```

## Sécurité

> ⚠️ Ce simulateur est destiné **uniquement** à des fins de démonstration et test.
> - Changer le token par défaut (`API_TOKEN`) avant tout déploiement
> - Ne pas utiliser avec des données réelles
> - Le service expose une API sans rate limiting

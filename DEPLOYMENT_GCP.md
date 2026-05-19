# Déploiement sur Google Cloud Platform — Guide complet

Ce guide couvre le déploiement du simulateur SentinelOne sur **Cloud Run** (GCP).
Cloud Run a été retenu comme seule option après expérience sur le projet similaire ProofPoint TAP : App Engine génère des problèmes de permissions complexes (bucket staging, service accounts) qui rallongent inutilement le déploiement.

---

## Table des matières

1. [Prérequis](#1-prérequis)
2. [Préparation du projet GCP](#2-préparation-du-projet-gcp)
3. [Déploiement Cloud Run](#3-déploiement-cloud-run)
4. [Problème fréquent : org policy bloquant l'accès public](#4-problème-fréquent--org-policy-bloquant-laccès-public)
5. [Configuration dans XSIAM](#5-configuration-dans-xsiam)
6. [Tests et validation](#6-tests-et-validation)
7. [Gestion courante](#7-gestion-courante)
8. [Dépannage](#8-dépannage)
9. [Coûts estimés](#9-coûts-estimés)
10. [Nettoyage](#10-nettoyage)

---

## 1. Prérequis

### Compte GCP
- Compte Google Cloud actif avec billing activé : https://console.cloud.google.com/billing
- Les nouveaux comptes ont **300 $ de crédits gratuits** — largement suffisant
- Coût estimé de ce simulateur : **< 1 $/mois** sur Cloud Run

### Google Cloud CLI (`gcloud`)

**Windows** — télécharger l'installateur :
https://cloud.google.com/sdk/docs/install#windows

**Mac** :
```bash
brew install --cask google-cloud-sdk
```

**Linux** :
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Vérification** :
```bash
gcloud --version
# Google Cloud SDK 460.0.0 (ou supérieur)
```

### Cloner le projet

```bash
git clone https://github.com/JCourtemanche/sentinelone-simul.git
cd sentinelone-simul
```

---

## 2. Préparation du projet GCP

### Étape 1 — Authentification

```bash
gcloud auth login
```
→ Une fenêtre de navigateur s'ouvre. Connectez-vous avec votre compte Google.

```bash
# Vérifier que vous êtes connecté
gcloud auth list
```

### Étape 2 — Créer ou sélectionner un projet GCP

**Option A : Créer un nouveau projet**

```bash
# Choisir un PROJECT_ID unique globalement sur GCP
export PROJECT_ID="sentinelone-sim-VOTRENOM"

gcloud projects create $PROJECT_ID \
  --name="SentinelOne Simulator"

gcloud config set project $PROJECT_ID
```

> ℹ️ Si l'ID est déjà pris, essayez `sentinelone-sim-demo-2025`, `s1-xsiam-sim-xyz`, etc.

**Option B : Utiliser un projet existant**

```bash
# Lister vos projets
gcloud projects list

# Sélectionner le projet
gcloud config set project VOTRE_PROJECT_ID
export PROJECT_ID=$(gcloud config get-value project)
```

### Étape 3 — Activer la facturation

```bash
# Lister vos comptes de facturation
gcloud billing accounts list

# Lier le projet (remplacer BILLING_ACCOUNT_ID par la valeur trouvée ci-dessus)
gcloud billing projects link $PROJECT_ID \
  --billing-account=BILLING_ACCOUNT_ID
```

Ou via la console : https://console.cloud.google.com/billing → sélectionner le projet → lier.

> ⚠️ **Sans billing, Cloud Build ne peut pas construire l'image.** C'est l'erreur la plus fréquente sur un projet neuf.

### Étape 4 — Définir la région

```bash
export REGION="europe-west1"
# Autres options : us-central1, europe-west4, asia-east1
```

---

## 3. Déploiement Cloud Run

### Option A : Script automatisé (recommandé)

```bash
cd sentinelone-simul
bash deploy-cloudrun.sh
```

Le script gère automatiquement :
1. Activation des APIs (Cloud Run, Cloud Build, Artifact Registry)
2. Création du repository Artifact Registry
3. Build de l'image Docker via Cloud Build
4. Déploiement sur Cloud Run
5. Tentative d'activation de l'accès public
6. Affichage de l'URL et des commandes de test

**Durée totale : environ 5 minutes pour le premier déploiement.**

---

### Option B : Déploiement manuel (étape par étape)

Si vous préférez contrôler chaque étape ou si le script échoue.

#### Étape 3.1 — Activer les APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

#### Étape 3.2 — Créer le repository Artifact Registry

```bash
gcloud artifacts repositories create sentinelone-simulator \
  --repository-format=docker \
  --location=$REGION \
  --description="SentinelOne API Simulator images"
```

#### Étape 3.3 — Construire l'image Docker

```bash
# Depuis la racine du projet (là où se trouve cloudbuild.yaml)
gcloud builds submit --config cloudbuild.yaml
```

> ℹ️ Cloud Build utilise le `cloudbuild.yaml` pour construire l'image depuis `deployment/Dockerfile`.
> La construction prend environ 2-3 minutes. Vous pouvez suivre l'avancement sur :
> https://console.cloud.google.com/cloud-build/builds

#### Étape 3.4 — Déployer sur Cloud Run

```bash
IMAGE_PATH="${REGION}-docker.pkg.dev/${PROJECT_ID}/sentinelone-simulator/s1-simulator:latest"

gcloud run deploy sentinelone-simulator \
  --image $IMAGE_PATH \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --min-instances 0 \
  --max-instances 2 \
  --set-env-vars API_TOKEN=test-api-token-sentinelone,DEBUG=False
```

#### Étape 3.5 — Activer l'accès public

```bash
gcloud run services add-iam-policy-binding sentinelone-simulator \
  --region=$REGION \
  --member=allUsers \
  --role=roles/run.invoker \
  --project=$PROJECT_ID
```

> ⚠️ Cette commande peut échouer si votre organisation a une policy qui bloque `allUsers`.
> **→ Voir la section 4 pour la solution.**

#### Étape 3.6 — Récupérer l'URL

```bash
gcloud run services describe sentinelone-simulator \
  --region $REGION \
  --format 'value(status.url)'
```

L'URL sera du type : `https://sentinelone-simulator-xxxxxxxxxx-ew.a.run.app`

---

## 4. Problème fréquent : org policy bloquant l'accès public

Ce problème survient dans les organisations GCP qui ont activé la contrainte `constraints/iam.allowedPolicyMemberDomains` ou `constraints/iam.disableServiceAccountKeyCreation`. Vous verrez une erreur comme :

```
ERROR: Policy update access denied.
One or more users named in the policy do not belong to a permitted customer.
```

ou le service déploie mais XSIAM reçoit une erreur `403 Forbidden`.

### Solution 1 : Service Account dédié pour XSIAM (recommandée)

Cette solution ne nécessite pas de modifier les policies d'organisation.

```bash
# 1. Créer un service account dédié
gcloud iam service-accounts create xsiam-s1-invoker \
  --display-name="XSIAM SentinelOne Simulator Invoker" \
  --project=$PROJECT_ID

# 2. Lui donner le droit d'invoquer Cloud Run
gcloud run services add-iam-policy-binding sentinelone-simulator \
  --region=$REGION \
  --member="serviceAccount:xsiam-s1-invoker@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/run.invoker"

# 3. Créer une clé JSON pour ce service account
gcloud iam service-accounts keys create xsiam-s1-key.json \
  --iam-account="xsiam-s1-invoker@${PROJECT_ID}.iam.gserviceaccount.com"
```

La clé `xsiam-s1-key.json` permet à XSIAM de s'authentifier auprès de GCP pour accéder au service.

> ⚠️ Conservez cette clé en lieu sûr. Ne la commitez pas sur GitHub.

### Solution 2 : Demander à l'admin GCP de modifier la policy

Si vous avez accès à l'administration de l'organisation GCP :

```bash
# Vérifier la policy actuelle
gcloud resource-manager org-policies describe \
  constraints/iam.allowedPolicyMemberDomains \
  --project=$PROJECT_ID

# Créer un fichier policy.yaml pour autoriser allUsers
cat > policy.yaml << 'EOF'
constraint: constraints/iam.allowedPolicyMemberDomains
listPolicy:
  allValues: ALLOW
EOF

# Appliquer (nécessite le rôle Organization Policy Administrator)
gcloud resource-manager org-policies set-policy \
  policy.yaml \
  --project=$PROJECT_ID
```

### Solution 3 : Cloud Run avec authentification via Identity Token

Si XSIAM supporte les Identity Tokens GCP (cas rare), vous pouvez tester :

```bash
# Générer un token d'identité pour tester
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Authorization: ApiToken test-api-token-sentinelone" \
  "https://VOTRE-SERVICE-URL/web/api/v2.1/agents"
```

---

## 5. Configuration dans XSIAM

### Étape 5.1 — Accéder à l'intégration

1. Dans XSIAM : **Settings** → **Integrations**
2. Rechercher **SentinelOne V2** (ou **SentinelOne V2 (Partner Contribution)**)
3. Cliquer **+ Add instance**

### Étape 5.2 — Paramètres de connexion

| Champ | Valeur |
|-------|--------|
| **Server URL** | URL Cloud Run (ex: `https://sentinelone-simulator-xxx-ew.a.run.app`) |
| **API Token** | `test-api-token-sentinelone` |
| **API Version** | `2.1` |
| **Trust any certificate** | Décoché (le certificat GCP est valide) |
| **Use system proxy settings** | Décoché |

> ⚠️ Ne pas mettre de `/` en fin d'URL. XSIAM construit les chemins comme :
> `{Server URL}/web/api/v2.1/agents`

### Étape 5.3 — Paramètres de collecte (Fetch Incidents)

| Champ | Valeur recommandée |
|-------|-------------------|
| **Fetch incidents** | ✅ Coché |
| **Fetch incidents from type** | `Both` (Threats + Alerts) ou `Threats` |
| **First fetch timestamp** | `3 days` |
| **Fetch limit** | `10` |
| **Minimum risk score** | `0` (simulateur génère tous les niveaux) |
| **Define which Alerts should be fetched** | `UNRESOLVED` |

### Étape 5.4 — Tester la connexion

Cliquer **Test** en bas du formulaire.

**Résultat attendu :** `Test passed`

Si vous obtenez une erreur :
- `401` → Vérifier le token (`Authorization: ApiToken test-api-token-sentinelone`)
- `403` → Problème d'org policy (voir section 4)
- `Connection refused` → URL incorrecte ou service non démarré
- `SSL error` → Cocher "Trust any certificate" temporairement pour tester

### Étape 5.5 — Sauvegarder

Cliquer **Save & exit**.

Après 1-2 minutes, les premiers incidents apparaissent dans **Incidents**.

---

## 6. Tests et validation

### Test rapide depuis votre terminal

```bash
# Remplacer par votre URL réelle
export SERVICE_URL="https://sentinelone-simulator-xxx-ew.a.run.app"
export TOKEN="test-api-token-sentinelone"

# Health check (pas d'auth requise)
curl "$SERVICE_URL/health"
# {"service": "SentinelOne API Simulator", "status": "healthy", ...}

# Agents
curl -H "Authorization: ApiToken $TOKEN" \
  "$SERVICE_URL/web/api/v2.1/agents" | python -m json.tool | head -30

# Menaces
curl -H "Authorization: ApiToken $TOKEN" \
  "$SERVICE_URL/web/api/v2.1/threats?limit=3" | python -m json.tool | head -50

# Alertes
curl -H "Authorization: ApiToken $TOKEN" \
  "$SERVICE_URL/web/api/v2.1/cloud-detection/alerts?limit=3" | python -m json.tool | head -50

# Test sans token (doit retourner 401)
curl -v "$SERVICE_URL/web/api/v2.1/agents"
# < HTTP/2 401
```

### Script de test complet

```bash
#!/bin/bash
SERVICE_URL="https://VOTRE-URL.run.app"
TOKEN="test-api-token-sentinelone"
H="Authorization: ApiToken $TOKEN"
OK=0; FAIL=0

test_endpoint() {
  local method=$1 url=$2 body=$3 desc=$4
  if [ "$method" = "POST" ]; then
    code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
      -H "$H" -H "Content-Type: application/json" \
      -d "${body:-{}}" "$SERVICE_URL$url")
  else
    code=$(curl -s -o /dev/null -w "%{http_code}" -H "$H" "$SERVICE_URL$url")
  fi
  if [ "$code" -lt 400 ]; then
    echo "✅ [$code] $desc"
    OK=$((OK+1))
  else
    echo "❌ [$code] $desc"
    FAIL=$((FAIL+1))
  fi
}

test_endpoint GET "/health" "" "Health check"
test_endpoint GET "/web/api/v2.1/agents" "" "List agents"
test_endpoint GET "/web/api/v2.1/threats" "" "List threats"
test_endpoint GET "/web/api/v2.1/cloud-detection/alerts" "" "List alerts"
test_endpoint GET "/web/api/v2.1/activities" "" "Activities"
test_endpoint GET "/web/api/v2.1/sites" "" "Sites"
test_endpoint GET "/web/api/v2.1/groups" "" "Groups"
test_endpoint GET "/web/api/v2.1/exclusions" "" "Exclusions (whitelist)"
test_endpoint GET "/web/api/v2.1/restrictions" "" "Restrictions (blocklist)"
test_endpoint GET "/web/api/v2.1/hashes/abc123def456/reputation" "" "Hash reputation"
test_endpoint POST "/web/api/v2.1/dv/init-query" '{"query":"test"}' "DV init-query"
test_endpoint GET "/web/api/v2.1/dv/events" "" "DV events"
test_endpoint GET "/web/api/v2.1/threat-intelligence/iocs" "" "IOCs"
test_endpoint GET "/web/api/v2.1/accounts" "" "Accounts"
test_endpoint POST "/web/api/v2.1/unifiedalerts/graphql" \
  '{"query":"{ alerts { edges { node { id } } } }"}' "UAM GraphQL"
test_endpoint GET "/web/api/v2.1/cloud-detection/rules" "" "STAR rules"
test_endpoint GET "/web/api/v2.1/service-users" "" "Service users"

echo ""
echo "Résultats : $OK OK, $FAIL échecs"
```

---

## 7. Gestion courante

### Voir les logs en temps réel

```bash
gcloud run services logs read sentinelone-simulator \
  --region $REGION \
  --tail

# Ou filtrer les erreurs uniquement
gcloud run services logs read sentinelone-simulator \
  --region $REGION \
  --filter="severity>=ERROR" \
  --limit=50
```

Via la console : https://console.cloud.google.com/logs → filtrer par `resource.type="cloud_run_revision"`

### Mettre à jour le simulateur

```bash
# Récupérer les modifications
git pull origin master

# Reconstruire et redéployer
gcloud builds submit --config cloudbuild.yaml

IMAGE_PATH="${REGION}-docker.pkg.dev/${PROJECT_ID}/sentinelone-simulator/s1-simulator:latest"
gcloud run services update sentinelone-simulator \
  --image $IMAGE_PATH \
  --region $REGION
```

### Changer le token d'API

```bash
gcloud run services update sentinelone-simulator \
  --set-env-vars API_TOKEN=mon-nouveau-token-secret,DEBUG=False \
  --region $REGION
```

Puis mettre à jour la configuration dans XSIAM (nouveau token).

### Ajuster le volume de données générées

```bash
# Générer entre 5 et 20 éléments par requête
gcloud run services update sentinelone-simulator \
  --set-env-vars MIN_ITEMS=5,MAX_ITEMS=20,API_TOKEN=test-api-token-sentinelone,DEBUG=False \
  --region $REGION
```

### Activer le mode debug temporairement

```bash
gcloud run services update sentinelone-simulator \
  --set-env-vars DEBUG=True,API_TOKEN=test-api-token-sentinelone \
  --region $REGION
```

> ⚠️ Désactiver après le débogage (logs très verbeux).

### Vérifier l'état du service

```bash
gcloud run services describe sentinelone-simulator --region $REGION
```

---

## 8. Dépannage

### ❌ Erreur : `Billing not enabled`

```
ERROR: (gcloud.builds.submit) FAILED_PRECONDITION: Billing is not enabled
```

**Solution :** Activer la facturation sur le projet.
```bash
gcloud billing accounts list
gcloud billing projects link $PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
```

---

### ❌ Erreur : `Permission denied` sur Cloud Build

```
ERROR: (gcloud.builds.submit) User does not have permission to access project [...]
```

**Solution :** Vérifier votre rôle sur le projet (vous devez être Editor ou Owner).
```bash
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:$(gcloud config get-value account)"
```

---

### ❌ Erreur : `403` depuis XSIAM après déploiement

XSIAM reçoit une erreur 403 sur toutes les requêtes.

**Cause probable :** L'org policy de votre organisation bloque l'accès `allUsers` à Cloud Run.

**Vérification :**
```bash
# Tester sans token GCP (doit retourner 403 si l'accès public est bloqué)
curl -v "https://VOTRE-SERVICE-URL/health"
```

**Solution :** Voir la [section 4](#4-problème-fréquent--org-policy-bloquant-laccès-public).

---

### ❌ Erreur : `401 Unauthorized` depuis XSIAM

XSIAM reçoit une erreur 401.

**Vérification :**
```bash
# Le header doit être exactement "Authorization: ApiToken <token>"
curl -v -H "Authorization: ApiToken test-api-token-sentinelone" \
  "https://VOTRE-SERVICE-URL/web/api/v2.1/agents"
```

**Causes possibles :**
- Token incorrect dans la config XSIAM → vérifier la variable `API_TOKEN` du service
- XSIAM envoie l'auth autrement (Bearer, Basic) → vérifier dans les logs

```bash
# Afficher la valeur actuelle du token configuré
gcloud run services describe sentinelone-simulator \
  --region $REGION \
  --format="value(spec.template.spec.containers[0].env)"
```

---

### ❌ Erreur : `Connection refused` ou timeout depuis XSIAM

**Causes possibles :**
1. URL incorrecte dans XSIAM (vérifier sans `/` final)
2. Service pas démarré → vérifier avec `gcloud run services list`
3. Proxy d'entreprise bloquant la connexion

```bash
# Vérifier que le service tourne
gcloud run services list --region $REGION

# Vérifier l'URL exacte
gcloud run services describe sentinelone-simulator \
  --region $REGION \
  --format 'value(status.url)'
```

---

### ❌ Erreur : `ModuleNotFoundError` dans les logs

```
ModuleNotFoundError: No module named 'faker'
```

**Cause :** Le `requirements.txt` n'a pas été copié correctement dans l'image Docker.

**Solution :** Vérifier que `deployment/Dockerfile` copie bien `simulator/requirements.txt` :
```dockerfile
COPY simulator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY simulator/ .
```

Puis relancer le build :
```bash
gcloud builds submit --config cloudbuild.yaml
```

---

### ❌ Cloud Build échoue avec `STEP_FAILED`

```bash
# Voir les logs du build
gcloud builds list --limit=5
gcloud builds log BUILD_ID
```

Cause fréquente : quota Cloud Build épuisé (120 min/jour gratuits) ou problème réseau GCP.
Attendre quelques minutes et relancer.

---

### ❌ Le service démarre mais répond des erreurs 500

**Vérifier les logs :**
```bash
gcloud run services logs read sentinelone-simulator \
  --region $REGION --limit=20
```

**Activer le debug et retester :**
```bash
gcloud run services update sentinelone-simulator \
  --set-env-vars DEBUG=True,API_TOKEN=test-api-token-sentinelone \
  --region $REGION
```

---

## 9. Coûts estimés

Cloud Run est **quasi gratuit** pour cet usage (démonstration, pas de production).

### Quotas gratuits mensuels
- **Requêtes** : 2 millions gratuites
- **CPU** : 180 000 vCPU-secondes
- **Mémoire** : 360 000 GiB-secondes

### Estimation pour une démo

| Scénario | Requêtes/jour | Coût estimé/mois |
|----------|--------------|-----------------|
| Tests ponctuels | < 500 | **Gratuit** |
| Démo active (8h/j) | < 5 000 | **< 0,50 $** |
| Intégration XSIAM fetch toutes les minutes | ~1 440 | **Gratuit** |

> ℹ️ Avec `--min-instances 0` (défaut), le service s'arrête quand il n'y a pas de trafic.
> Un "cold start" peut prendre 2-3 secondes à la première requête après une période d'inactivité.
> Pour XSIAM, cela n'est pas problématique car les requêtes sont répétées régulièrement.

---

## 10. Nettoyage

### Supprimer uniquement le service Cloud Run

```bash
gcloud run services delete sentinelone-simulator --region $REGION
```

### Supprimer l'image Docker

```bash
gcloud artifacts repositories delete sentinelone-simulator \
  --location=$REGION \
  --quiet
```

### Supprimer tout le projet GCP

> ⚠️ Irréversible après 30 jours. Supprime **toutes** les ressources du projet.

```bash
gcloud projects delete $PROJECT_ID
```

Vous avez 30 jours pour annuler via : https://console.cloud.google.com/iam-admin/projects

---

## Ressources

- **Console GCP** : https://console.cloud.google.com
- **Cloud Run** : https://cloud.google.com/run/docs
- **Cloud Build** : https://cloud.google.com/build/docs
- **Calculateur de prix** : https://cloud.google.com/products/calculator
- **Logs** : https://console.cloud.google.com/logs
- **Documentation SentinelOne V2 (XSIAM)** : https://xsoar.pan.dev/docs/reference/integrations/sentinel-one-v2

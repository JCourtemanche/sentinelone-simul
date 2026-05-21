# Déploiement GCP — SentinelOne Simulator

## Procédure de déploiement

### 1. Ouvrir Cloud Shell

Dans la [console GCP](https://console.cloud.google.com/), sélectionne ton projet puis clique sur l'icône **Cloud Shell** en haut à droite.

### 2. Cloner le projet

```bash
git clone https://github.com/JCourtemanche/sentinelone-simul
```

### 3. Se déplacer dans le répertoire

```bash
cd sentinelone-simul
```

### 4. Lancer le déploiement

```bash
bash deploy-cloudrun.sh
```

Le script gère automatiquement :
- Activation des APIs GCP nécessaires
- Création du repository Artifact Registry
- Build de l'image Docker via Cloud Build
- Déploiement sur Cloud Run

À la fin, l'URL du service est affichée.

### 5. Autoriser l'accès public

Dans la [console Cloud Run](https://console.cloud.google.com/run), ouvre le service **sentinelone-simulator**, va dans l'onglet **Sécurité** et vérifie que **Authentification** est réglé sur **Autoriser l'accès non authentifié**.

> Si cette option est grisée, une policy d'organisation GCP bloque l'accès public.  
> Contacte ton admin GCP pour qu'il autorise `constraints/iam.allowedPolicyMemberDomains` sur ce projet.

---

## Validation

```bash
SERVICE_URL="https://sentinelone-simulator-XXXX-ew.a.run.app"  # URL affichée à l'étape 4

# Health check
curl $SERVICE_URL/health

# Test agents
curl -H "Authorization: ApiToken test-api-token-sentinelone" \
  "$SERVICE_URL/web/api/v2.1/agents"

# Test threats
curl -H "Authorization: ApiToken test-api-token-sentinelone" \
  "$SERVICE_URL/web/api/v2.1/threats"
```

## Configuration XSIAM (SentinelOne V2)

| Champ | Valeur |
|---|---|
| Server URL | URL Cloud Run |
| API Token | `test-api-token-sentinelone` |
| API Version | `2.1` |

## Commandes utiles

```bash
# Voir les logs
gcloud run services logs read sentinelone-simulator --region europe-west1

# Redéployer après une mise à jour du code
git pull && bash deploy-cloudrun.sh

# Supprimer le service
gcloud run services delete sentinelone-simulator --region europe-west1
```

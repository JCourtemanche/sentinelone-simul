#!/bin/bash
# Script de déploiement Cloud Run pour le simulateur SentinelOne
# Usage: bash deploy-cloudrun.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
REGION="europe-west1"
SERVICE_NAME="sentinelone-simulator"
REPO_NAME="sentinelone-simulator"

echo -e "${GREEN}=== Déploiement Cloud Run - Simulateur SentinelOne ===${NC}\n"
echo -e "${YELLOW}Project:${NC} $PROJECT_ID"
echo -e "${YELLOW}Region:${NC} $REGION"
echo -e "${YELLOW}Service:${NC} $SERVICE_NAME"
echo ""

# 1. Activer les APIs
echo -e "${YELLOW}[1/6] Activation des APIs...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
echo -e "${GREEN}✓ APIs activées${NC}\n"

# 2. Créer le repository Artifact Registry
echo -e "${YELLOW}[2/6] Configuration d'Artifact Registry...${NC}"
REPO_EXISTS=$(gcloud artifacts repositories list \
  --location=$REGION \
  --filter="name:$REPO_NAME" \
  --format="value(name)" 2>/dev/null)

if [ -z "$REPO_EXISTS" ]; then
  gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="SentinelOne API Simulator images" \
    --quiet
  echo -e "${GREEN}✓ Repository créé${NC}"
else
  echo -e "${GREEN}✓ Repository existe déjà${NC}"
fi
echo ""

# 3. Vérifier le Dockerfile
echo -e "${YELLOW}[3/6] Vérification du répertoire...${NC}"
if [ ! -f "deployment/Dockerfile" ]; then
    echo -e "${RED}ERREUR: Dockerfile non trouvé${NC}"
    echo "Assurez-vous d'être dans le répertoire sentinelone-simul"
    exit 1
fi
echo -e "${GREEN}✓ Dockerfile trouvé${NC}\n"

# 4. Construire l'image
echo -e "${YELLOW}[4/6] Construction de l'image Docker...${NC}"
echo "Cela peut prendre 2-3 minutes..."
gcloud builds submit --config cloudbuild.yaml

IMAGE_PATH="${REGION}-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/s1-simulator:latest"
echo -e "${GREEN}✓ Image construite: $IMAGE_PATH${NC}\n"

# 5. Déployer sur Cloud Run
echo -e "${YELLOW}[5/6] Déploiement sur Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
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

# 6. Accès public
echo -e "${YELLOW}[6/6] Configuration de l'accès public...${NC}"
gcloud run services add-iam-policy-binding $SERVICE_NAME \
  --region=$REGION \
  --member=allUsers \
  --role=roles/run.invoker \
  --project=$PROJECT_ID \
  --quiet 2>/dev/null && PUBLIC_ACCESS=true || PUBLIC_ACCESS=false

if [ "$PUBLIC_ACCESS" = true ]; then
  echo -e "${GREEN}✓ Accès public activé${NC}\n"
else
  echo -e "${YELLOW}⚠ Accès public bloqué par policy d'organisation${NC}\n"
fi

# URL du service
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --region $REGION \
  --format 'value(status.url)')

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Déploiement réussi !${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}URL du service:${NC} ${GREEN}$SERVICE_URL${NC}"
echo ""
echo -e "${YELLOW}Tests de validation:${NC}"
echo ""
echo "1. Health check:"
echo -e "   ${GREEN}curl $SERVICE_URL/health${NC}"
echo ""
echo "2. Test agents:"
echo -e "   ${GREEN}curl -H 'Authorization: ApiToken test-api-token-sentinelone' \\${NC}"
echo -e "     ${GREEN}\"$SERVICE_URL/web/api/v2.1/agents\"${NC}"
echo ""
echo "3. Test threats:"
echo -e "   ${GREEN}curl -H 'Authorization: ApiToken test-api-token-sentinelone' \\${NC}"
echo -e "     ${GREEN}\"$SERVICE_URL/web/api/v2.1/threats\"${NC}"
echo ""
echo -e "${YELLOW}Configuration XSIAM (SentinelOne V2):${NC}"
echo "   Server URL: $SERVICE_URL"
echo "   API Token:  test-api-token-sentinelone"
echo "   API Version: 2.1"
echo ""
echo -e "${YELLOW}Commandes utiles:${NC}"
echo "   Voir les logs:  gcloud run services logs read $SERVICE_NAME --region $REGION"
echo "   Supprimer:      gcloud run services delete $SERVICE_NAME --region $REGION"
echo ""

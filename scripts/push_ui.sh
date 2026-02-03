#!/bin/bash

# Función para verificar variables obligatorias
check_var() {
    if [ -z "${!1}" ]; then
        echo "❌ Error: La variable de entorno $1 no está definida."
        exit 1
    fi
}

# Validamos que el entorno provea toda la metadata
check_var "GCP_PROJECT_ID"
check_var "GCP_REGION"
check_var "GCP_REPO_NAME"
check_var "GCP_IMAGE_NAME"
check_var "PYTHON_VERSION"
check_var "APP_PORT"

# Variables dinámicas
TAG=$(git rev-parse --short HEAD 2>/dev/null || echo "latest")
REGISTRY_HOST="${GCP_REGION}-docker.pkg.dev"
IMAGE_URL="${REGISTRY_HOST}/${GCP_PROJECT_ID}/${GCP_REPO_NAME}/${GCP_IMAGE_NAME}:${TAG}"

echo "🛠️ Construyendo imagen: ${GCP_IMAGE_NAME}:${TAG}"

docker build \
  --build-arg PYTHON_VERSION="$PYTHON_VERSION" \
  --build-arg APP_PORT="$APP_PORT" \
  -t "$IMAGE_URL" -f apps/frontend/Dockerfile .

echo "📤 Subiendo a Artifact Registry..."
docker push "$IMAGE_URL"
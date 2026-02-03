# Autonomous Data Analyst: Python + Google Cloud

## Configuración de Seguridad (GitHub Secrets)

Para que este proyecto sea funcional, debes configurar los siguientes Secretos en tu repositorio de GitHub (`Settings > Secrets and variables > Actions`):

| Secreto | Descripción |
| :--- | :--- |
| `GCP_PROJECT_ID` | El ID único de tu proyecto en Google Cloud. |
| `GCP_PROJECT_NUMBER` | El número identificador del proyecto (12 dígitos). |
| `GCP_REGION` | Región por defecto (ej. us-central1). |
| `WIF_PROVIDER` | El ID completo del Workload Identity Provider. |
| `WIF_SERVICE_ACCOUNT` | El ID completo del Workload Identity Service Account. |

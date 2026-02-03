variable "project_id" {
  description = "ID del proyecto de GCP"
  type        = string
}

variable "gcp_service_list" {
  description = "Lista de APIs a habilitar"
  type        = list(string)
  default = [
    "compute.googleapis.com",         # Redes e IPs
    "run.googleapis.com",             # Cloud Run
    "iam.googleapis.com",             # Permisos e IAM
    "iap.googleapis.com",             # Identity-Aware Proxy
    "artifactregistry.googleapis.com" # Docker Images
  ]
}

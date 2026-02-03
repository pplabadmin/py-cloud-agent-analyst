variable "project_id" {
  type        = string
  description = "ID del proyecto de GCP"
}

variable "app_service_account_name" {
  type        = string
  description = "Nombre único para la Service Account de la aplicación"
}

variable "github_pool_id" {
  type    = string
  default = "github-actions-pool"
}

variable "github_repository" {
  description = "Formato: usuario/repo"
  type        = string
}

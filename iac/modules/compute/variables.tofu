variable "project_id" { type = string }
variable "region" { type = string }

variable "repository_id" {
  description = "Nombre del repositorio en Artifact Registry"
  type        = string
}

variable "service_name" {
  description = "Nombre del servicio de Cloud Run"
  type        = string
}

variable "container_image" {
  description = "URL de la imagen de Docker (placeholder si aún no existe)"
  type        = string
}

variable "service_account_email" {
  description = "Email de la SA que creamos en el módulo de IAM"
  type        = string
}

variable "external_ip_address" {
  description = "La dirección IP estática que reservamos en networking"
  type        = string
}

variable "domain_name" {
  type        = string
  description = "El dominio para el certificado"
}

variable "iap_client_id" { type = string }

variable "iap_client_secret" {
  type      = string
  sensitive = true
}

variable "admin_email" { type = string }

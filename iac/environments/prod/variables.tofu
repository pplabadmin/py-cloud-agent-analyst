variable "project_id" {
  description = "El ID del proyecto de GCP"
  type        = string
}

variable "region" {
  description = "Región por defecto para los recursos"
  type        = string
}

variable "vpc_name" {
  description = "Nombre de la red VPC"
  type        = string
}

variable "auto_create_subnetworks" {
  description = "Define si se crean subredes automáticamente"
  type        = bool
}

variable "subnet_cidr" {
  description = "Rango de IPs para la subred"
  type        = string
}

variable "ip_name" {
  description = "Nombre para la IP estática"
  type        = string
}

variable "ip_address_type" {
  description = "Tipo de dirección (EXTERNAL o INTERNAL)"
  type        = string
}

variable "ip_version" {
  description = "Versión de IP (IPV4 o IPV6)"
  type        = string
}

variable "app_service_account_name" {
  type = string
}

variable "repository_id" {
  type = string
}

variable "service_name" {
  type = string
}

variable "container_image" {
  type = string
}

variable "domain_name" {
  type = string
}

variable "iap_client_id" {
  type = string
}

variable "iap_client_secret" {
  type      = string
  sensitive = true
}

variable "admin_email" {
  type = string
}

variable "github_repository" {
  description = "Repositorio en formato usuario/repo"
  type        = string
}

variable "github_pool_id" {
  description = "ID del pool para Workload Identity"
  type        = string
}

variable "project_id" {
  description = "ID del proyecto de GCP"
  type        = string
}

variable "region" {
  description = "Región para los recursos regionales"
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

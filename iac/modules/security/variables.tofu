variable "project_id" {
  type = string
}

variable "support_email" {
  description = "Email de soporte para la pantalla de OAuth (debe ser tu correo)"
  type        = string
}

variable "application_title" {
  description = "Nombre que verán los usuarios al loguearse"
  type        = string
}

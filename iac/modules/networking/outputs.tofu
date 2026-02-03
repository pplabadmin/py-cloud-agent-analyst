output "static_ip_address" {
  value       = google_compute_global_address.lb_static_ip.address
  description = "La IP pública global que debes configurar en AWS Route53 (Registro A)."
}

output "vpc_id" {
  value       = google_compute_network.main_vpc.id
  description = "El ID de la red VPC para ser usado por otros módulos."
}

output "subnet_id" {
  value       = google_compute_subnetwork.main_subnet.id
  description = "El ID de la subred para el despliegue de recursos regionales."
}

output "network_name" {
  value       = google_compute_network.main_vpc.name
  description = "El nombre de la red VPC."
}

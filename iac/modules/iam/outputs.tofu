output "app_sa_email" {
  value       = google_service_account.app_sa.email
  description = "El email de la Service Account creada para la aplicación"
}

output "workload_identity_provider" {
  value = google_iam_workload_identity_pool_provider.github_provider.name
}

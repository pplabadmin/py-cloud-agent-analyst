output "IP_PARA_AWS_ROUTE53" {
  value = module.networking.static_ip_address
}

output "workload_identity_provider" {
  description = "ID del provider para configurar en el deploy-ui.yml de GitHub"
  value       = module.iam.workload_identity_provider
}

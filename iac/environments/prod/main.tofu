module "services" {
  source     = "../../modules/services"
  project_id = var.project_id
}

resource "time_sleep" "wait_api_propagation" {
  depends_on = [module.services]

  create_duration = "60s"
}

module "networking" {
  source                  = "../../modules/networking"
  project_id              = var.project_id
  region                  = var.region
  vpc_name                = var.vpc_name
  auto_create_subnetworks = var.auto_create_subnetworks
  subnet_cidr             = var.subnet_cidr
  ip_name                 = var.ip_name
  ip_address_type         = var.ip_address_type
  ip_version              = var.ip_version

  depends_on = [time_sleep.wait_api_propagation]
}

module "iam" {
  source                   = "../../modules/iam"
  project_id               = var.project_id
  app_service_account_name = var.app_service_account_name
  github_repository        = var.github_repository
  github_pool_id           = var.github_pool_id

  depends_on = [module.services]
}

module "compute" {
  source                = "../../modules/compute"
  project_id            = var.project_id
  region                = var.region
  repository_id         = var.repository_id
  service_name          = var.service_name
  container_image       = var.container_image
  domain_name           = var.domain_name
  service_account_email = module.iam.app_sa_email
  external_ip_address   = module.networking.static_ip_address

  iap_client_id     = var.iap_client_id
  iap_client_secret = var.iap_client_secret
  admin_email       = var.admin_email

  depends_on = [module.iam, module.networking, module.services]
}

output "public_ip_for_aws" {
  value = module.networking.static_ip_address
}

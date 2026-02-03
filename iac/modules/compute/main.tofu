# 1. Certificado SSL Gestionado por Google
resource "google_compute_managed_ssl_certificate" "default" {
  name    = "${var.service_name}-cert"
  project = var.project_id
  managed {
    domains = [var.domain_name]
  }
}

# 2. Repositorio para tus imágenes
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.repository_id
  format        = "DOCKER"
  project       = var.project_id
}

# 3. Servicio de Cloud Run
resource "google_cloud_run_v2_service" "app" {
  name                = var.service_name
  location            = var.region
  project             = var.project_id
  deletion_protection = false

  template {
    service_account = var.service_account_email
    containers {
      image = var.container_image
      resources {
        limits = {
          cpu    = "1"
          memory = "2Gi"
        }
      }
      ports { container_port = 8080 }
    }
  }
}

# 4. Serverless Network Endpoint Group (NEG)
# Esto permite que el Load Balancer "vea" a Cloud Run
resource "google_compute_region_network_endpoint_group" "cloudrun_neg" {
  name                  = "${var.service_name}-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  project               = var.project_id
  cloud_run {
    service = google_cloud_run_v2_service.app.name
  }
}

# 5. Backend Service para el Load Balancer
resource "google_compute_backend_service" "default" {
  name                  = "${var.service_name}-backend"
  project               = var.project_id
  protocol              = "HTTP"
  port_name             = "http"
  timeout_sec           = 30
  load_balancing_scheme = "EXTERNAL_MANAGED"

  backend {
    group = google_compute_region_network_endpoint_group.cloudrun_neg.id
  }

  iap {
    enabled              = true
    oauth2_client_id     = var.iap_client_id
    oauth2_client_secret = var.iap_client_secret
  }
}

resource "google_iap_web_backend_service_iam_member" "access" {
  project             = var.project_id
  web_backend_service = google_compute_backend_service.default.name
  role                = "roles/iap.httpsResourceAccessor"
  member              = "user:${var.admin_email}"
}

# 6. URL Map (Reglas de ruteo)
resource "google_compute_url_map" "default" {
  name            = "${var.service_name}-url-map"
  project         = var.project_id
  default_service = google_compute_backend_service.default.id
}

# 7. Proxy HTTP (Para recibir tráfico)
resource "google_compute_target_https_proxy" "default" {
  name             = "${var.service_name}-https-proxy"
  project          = var.project_id
  url_map          = google_compute_url_map.default.id
  ssl_certificates = [google_compute_managed_ssl_certificate.default.id]
}

# 8. Forwarding Rule (El que amarra la IP con el balanceador)
resource "google_compute_global_forwarding_rule" "default" {
  name                  = "${var.service_name}-forwarding-rule"
  project               = var.project_id
  target                = google_compute_target_https_proxy.default.id
  port_range            = "443"
  ip_address            = var.external_ip_address
  load_balancing_scheme = "EXTERNAL_MANAGED"
}

resource "google_cloud_run_v2_service_iam_member" "allow_iap_traffic" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.app.name
  role     = "roles/run.invoker"
  member   = "allAuthenticatedUsers"
}

resource "google_project_service_identity" "iap_sa" {
  provider = google-beta
  project  = var.project_id
  service  = "iap.googleapis.com"
}

resource "google_cloud_run_v2_service_iam_member" "iap_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.app.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_project_service_identity.iap_sa.email}"
}

resource "google_iap_client" "project_client" {
  display_name = var.application_title
  brand        = "projects/${var.project_id}/brands/${var.project_id}"
}

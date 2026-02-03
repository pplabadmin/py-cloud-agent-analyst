resource "google_compute_network" "main_vpc" {
  name                    = var.vpc_name
  project                 = var.project_id
  auto_create_subnetworks = var.auto_create_subnetworks
}

resource "google_compute_subnetwork" "main_subnet" {
  name          = "${var.vpc_name}-subnet"
  project       = var.project_id
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.main_vpc.id
}

resource "google_compute_global_address" "lb_static_ip" {
  name         = var.ip_name
  project      = var.project_id
  address_type = var.ip_address_type
  ip_version   = var.ip_version
}

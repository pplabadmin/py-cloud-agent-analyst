terraform {
  required_version = ">= 1.11.5"

  required_providers {
    google = {
      source  = "opentofu/google"
      version = "7.20.0"
    }

    time = {
      source  = "hashicorp/time"
      version = "0.13.1"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

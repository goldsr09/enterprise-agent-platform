terraform {
  required_version = "= 1.16.3"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "= 8.3.0"
    }
  }
}

provider "google" {
  project = "seventh-azimuth-430506-q5"
  region  = "us-central1"
}

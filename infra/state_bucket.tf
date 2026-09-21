resource "google_storage_bucket" "terraform_state" {
  project  = var.project_id
  name     = "seventh-azimuth-430506-q5-terraform-state"
  location = "US-CENTRAL1"

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  versioning {
    enabled = true
  }

  lifecycle {
    prevent_destroy = true
  }
}
terraform {
  backend "gcs" {
    bucket = "seventh-azimuth-430506-q5-terraform-state"
    prefix = "enterprise-agent-platform/staging"
  }
}

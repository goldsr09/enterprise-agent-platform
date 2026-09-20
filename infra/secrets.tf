resource "google_project_service" "secret_manager" {
  project = var.project_id
  service = "secretmanager.googleapis.com"

  disable_on_destroy = false
}

resource "google_secret_manager_secret" "openai_api_key" {
  project   = var.project_id
  secret_id = "enterprise-agent-openai-api-key"

  replication {
    auto {}
  }

  depends_on = [
    google_project_service.secret_manager
  ]
}

resource "google_secret_manager_secret" "database_password" {
  project   = var.project_id
  secret_id = "enterprise-agent-database-password"

  replication {
    auto {}
  }

  depends_on = [
    google_project_service.secret_manager
  ]
}
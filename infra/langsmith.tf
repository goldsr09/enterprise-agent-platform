resource "google_secret_manager_secret" "langsmith_api_key" {
  project   = var.project_id
  secret_id = "enterprise-agent-langsmith-api-key"

  replication {
    auto {}
  }

  depends_on = [google_project_service.secret_manager]
}

resource "google_secret_manager_secret_iam_member" "api_langsmith_key" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.langsmith_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.api.email}"
}

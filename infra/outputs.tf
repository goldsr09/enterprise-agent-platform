output "registry_url" {
  description = "Registry address used when tagging and pushing images."
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.app.repository_id}"
}

output "database_connection_name" {
  description = "Cloud SQL connection name."
  value       = google_sql_database_instance.postgres.connection_name
}

output "api_url" {
  description = "API URL, available after enabling deployment."
  value       = try(google_cloud_run_v2_service.api[0].uri, null)
}
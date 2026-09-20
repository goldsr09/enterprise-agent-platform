resource "google_project_service" "cloud_sql" {
  project = var.project_id
  service = "sqladmin.googleapis.com"

  disable_on_destroy = false
}

resource "google_sql_database_instance" "postgres" {
  project          = var.project_id
  name             = "enterprise-agent-postgres"
  region           = var.region
  database_version = "POSTGRES_16"

  deletion_protection = true

  settings {
    edition           = "ENTERPRISE"
    tier              = "db-f1-micro"
    availability_type = "ZONAL"
    disk_size         = 10
    disk_type         = "PD_SSD"

    ip_configuration {
      ipv4_enabled = true
    }
  }

  depends_on = [
    google_project_service.cloud_sql
  ]
}

resource "google_sql_database" "agent" {
  project  = var.project_id
  name     = "agent_db"
  instance = google_sql_database_instance.postgres.name
}
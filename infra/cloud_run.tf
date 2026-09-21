resource "google_project_service" "cloud_run" {
  project = var.project_id
  service = "run.googleapis.com"

  disable_on_destroy = false
}

resource "google_cloud_run_v2_service" "api" {
  count = var.deploy_api ? 1 : 0

  project  = var.project_id
  name     = "enterprise-agent-api"
  location = var.region

  deletion_protection = false

  template {
    service_account       = google_service_account.api.email
    execution_environment = "EXECUTION_ENVIRONMENT_GEN2"

    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }

    containers {
      image = var.api_image

      ports {
        container_port = 8000
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
      }

      env {
        name  = "LANGSMITH_TRACING"
        value = "true"
      }

      env {
        name  = "LANGSMITH_PROJECT"
        value = "enterprise-agent-platform-production"
      }

      env {
        name = "LANGSMITH_API_KEY"

        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.langsmith_api_key.secret_id
            version = "1"
          }
        }
      }

      env {
        name  = "DB_HOST"
        value = "/cloudsql/${google_sql_database_instance.postgres.connection_name}"
      }

      env {
        name  = "DB_PORT"
        value = "5432"
      }

      env {
        name  = "DB_NAME"
        value = google_sql_database.agent.name
      }

      env {
        name  = "DB_USER"
        value = "agent_user"
      }

      env {
        name = "DB_PASSWORD"

        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.database_password.secret_id
            version = "1"
          }
        }
      }

      env {
        name = "OPENAI_API_KEY"

        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.openai_api_key.secret_id
            version = "2"
          }
        }
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
    }

    volumes {
      name = "cloudsql"

      cloud_sql_instance {
        instances = [
          google_sql_database_instance.postgres.connection_name
        ]
      }
    }
  }

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
    precondition {
      condition     = trimspace(var.api_image) != ""
      error_message = "Set api_image before enabling deploy_api."
    }
  }

  depends_on = [
    google_project_service.cloud_run,
    google_project_iam_member.api_cloud_sql,
    google_secret_manager_secret_iam_member.api_openai_key,
    google_secret_manager_secret_iam_member.api_database_password,
    google_secret_manager_secret_iam_member.api_langsmith_key
  ]
}
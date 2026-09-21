resource "google_project_service" "github_auth" {
  for_each = toset([
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
  ])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_service_account" "github_deployer" {
  project      = var.project_id
  account_id   = "github-deployer"
  display_name = "GitHub Actions deployment"

  depends_on = [google_project_service.iam]
}

resource "google_iam_workload_identity_pool" "github" {
  project                   = var.project_id
  workload_identity_pool_id = "github-actions"
  display_name              = "GitHub Actions"

  depends_on = [
    google_project_service.iam,
    google_project_service.github_auth,
  ]
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  display_name                       = "GitHub repository"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"                = "assertion.sub"
    "attribute.repository_id"       = "assertion.repository_id"
    "attribute.repository_owner_id" = "assertion.repository_owner_id"
    "attribute.ref"                 = "assertion.ref"
  }

  attribute_condition = <<-EOT
    assertion.repository_owner_id == '18200239' &&
    assertion.repository_id == '1377624574' &&
    assertion.ref == 'refs/heads/main'
  EOT
}

resource "google_service_account_iam_member" "github_identity" {
  service_account_id = google_service_account.github_deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository_id/1377624574"

  depends_on = [google_iam_workload_identity_pool_provider.github]
}

output "github_workload_identity_provider" {
  value = google_iam_workload_identity_pool_provider.github.name
}

output "github_deployer_email" {
  value = google_service_account.github_deployer.email
}

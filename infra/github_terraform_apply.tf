resource "google_service_account" "github_terraform_apply" {
  project      = var.project_id
  account_id   = "github-terraform-apply"
  display_name = "GitHub Terraform apply"

  depends_on = [google_project_service.iam]
}

resource "google_service_account_iam_member" "github_terraform_apply_identity" {
  service_account_id = google_service_account.github_terraform_apply.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository_id/1377624574"

  depends_on = [google_iam_workload_identity_pool_provider.github]
}

output "github_terraform_apply_email" {
  value = google_service_account.github_terraform_apply.email
}

resource "google_project_iam_member" "terraform_apply_read" {
  for_each = toset([
    "roles/viewer",
    "roles/iam.securityReviewer",
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.github_terraform_apply.email}"
}

resource "google_storage_bucket_iam_member" "terraform_apply_state" {
  bucket = google_storage_bucket.terraform_state.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.github_terraform_apply.email}"
}

resource "google_cloud_run_v2_service_iam_member" "terraform_apply_services" {
  for_each = {
    api = google_cloud_run_v2_service.api[0].name
    mcp = google_cloud_run_v2_service.mcp.name
  }

  project  = var.project_id
  location = var.region
  name     = each.value
  role     = "roles/run.developer"
  member   = "serviceAccount:${google_service_account.github_terraform_apply.email}"
}

resource "google_service_account_iam_member" "terraform_apply_act_as" {
  service_account_id = google_service_account.api.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.github_terraform_apply.email}"
}
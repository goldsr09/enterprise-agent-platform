resource "google_service_account" "github_terraform_plan" {
  project      = var.project_id
  account_id   = "github-terraform-plan"
  display_name = "GitHub Terraform planning"

  depends_on = [google_project_service.iam]
}

resource "google_service_account_iam_member" "github_terraform_identity" {
  service_account_id = google_service_account.github_terraform_plan.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository_id/1377624574"

  depends_on = [google_iam_workload_identity_pool_provider.github]
}

resource "google_project_iam_member" "terraform_plan_read" {
  for_each = toset([
    "roles/viewer",
    "roles/iam.securityReviewer",
  ])

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.github_terraform_plan.email}"
}

resource "google_storage_bucket_iam_member" "terraform_plan_state" {
  bucket = google_storage_bucket.terraform_state.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.github_terraform_plan.email}"
}

output "github_terraform_plan_email" {
  value = google_service_account.github_terraform_plan.email
}
variable "project_id" {
  description = "Google Cloud project hosting the application."
  type        = string
  default     = "seventh-azimuth-430506-q5"
}

variable "region" {
  description = "Google Cloud region for the application."
  type        = string
  default     = "us-central1"
}

variable "deploy_api" {
  description = "Deploy the API after its image and secrets are ready."
  type        = bool
  default     = false
}

variable "api_image" {
  description = "Full Artifact Registry image address."
  type        = string
  default     = ""
}
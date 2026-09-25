resource "google_sql_database" "staging" {
  project  = "seventh-azimuth-430506-q5"
  name     = "agent_staging_db"
  instance = "enterprise-agent-postgres"
}
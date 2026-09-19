# Data Ingestion Investigation

If sessions fall sharply for a single platform:

1. Check whether event ingestion volume declined.
2. Check for recent SDK releases on that platform.
3. Check the data pipeline for failed or delayed jobs.
4. Check API authentication and authorization errors.
5. Compare the affected platform with unaffected platforms.

A decline in sessions may indicate an ingestion problem, but metrics
alone do not prove the cause. Confirm the diagnosis using logs,
deployment history, and pipeline health.
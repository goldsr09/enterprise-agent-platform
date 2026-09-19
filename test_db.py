from app.tools.sql_tool import get_metrics

rows = get_metrics(
    "Android",
    "2026-09-15",
    "2026-09-16"
)

for row in rows:
    print(row)
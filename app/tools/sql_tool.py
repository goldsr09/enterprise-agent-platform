from app.db.connection import get_connection
from psycopg.rows import dict_row
from langchain_core.tools import tool


def get_metrics(platform: str, start_date: str, end_date: str):
    conn = get_connection()
    cursor = conn.cursor(row_factory=dict_row)


    cursor.execute("""
        SELECT date, platform, country, revenue, sessions
        FROM metrics
        WHERE platform = %s
            AND date between %s AND %s
        ORDER BY date;
    """, (platform,start_date,end_date))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


@tool
def get_metrics_tool(platform: str,start_date: str,end_date: str):
    """Get revenue and session metrics for a platform over a date range."""

    return get_metrics(
        platform,
        start_date,
        end_date
        )


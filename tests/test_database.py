import unittest
from datetime import date

from app.db.connection import get_connection


class DatabaseTests(unittest.TestCase):
    def test_android_sessions_for_date_range(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT date, sessions
                    FROM metrics
                    WHERE platform = %s
                      AND date BETWEEN %s AND %s
                    ORDER BY date
                    """,
                    ("Android", "2026-09-15", "2026-09-16"),
                )
                rows = cursor.fetchall()

        self.assertEqual(
            rows,
            [
                (date(2026, 9, 15), 720000),
                (date(2026, 9, 16), 350000),
            ],
        )

    def test_unknown_platform_returns_no_rows(self):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT sessions FROM metrics WHERE platform = %s",
                    ("BlackBerry",),
                )
                rows = cursor.fetchall()

        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()

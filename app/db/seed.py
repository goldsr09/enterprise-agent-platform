from app.db.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS metrics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    platform TEXT NOT NULL,
    country TEXT NOT NULL,
    revenue NUMERIC NOT NULL,
    sessions INTEGER NOT NULL
);
""")

# For now, reset the demo data every time we seed
cursor.execute("DELETE FROM metrics;")

rows = [
    ("2026-09-15", "iOS", "US", 120000, 800000),
    ("2026-09-15", "Android", "US", 95000, 720000),
    ("2026-09-16", "iOS", "US", 118000, 790000),
    ("2026-09-16", "Android", "US", 43000, 350000),
]

cursor.executemany("""
INSERT INTO metrics (date, platform, country, revenue, sessions)
VALUES (%s, %s, %s, %s, %s);
""", rows)

conn.commit()

cursor.close()
conn.close()

print("metrics table seeded")
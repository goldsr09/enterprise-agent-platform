import os
from dotenv import load_dotenv

import psycopg

def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST","localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "agent_db"),
        user=os.getenv("DB_USER", "agent_user"),
        password=os.getenv("DB_PASSWORD", "agent_password"),
        connect_timeout=5
    )


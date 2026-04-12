import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_PASSWORD = os.getenv("VIP_PASSWORD")
DB_URL = os.getenv("DB_URL")


def get_db_cursor():
    connect = psycopg2.connect(DB_URL)
    cursor = connect.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Passwords(
        id SERIAL PRIMARY KEY,
        original_message TEXT,
        type TEXT,
        result TEXT
    )
    """)
    connect.commit()
    return connect, cursor

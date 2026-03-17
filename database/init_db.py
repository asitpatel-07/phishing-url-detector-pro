import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import ensure_directories, get_db_connection, get_current_timestamp


def init_database():
    ensure_directories()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            url TEXT NOT NULL,
            prediction TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            phishing_confidence REAL NOT NULL,
            legitimate_confidence REAL NOT NULL,
            severity TEXT NOT NULL,
            domain_resolves TEXT,
            http_status TEXT,
            scan_time TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blacklist_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            source TEXT DEFAULT 'manual',
            added_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocked_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            risk_score INTEGER NOT NULL,
            blocked_at TEXT NOT NULL,
            blocked_until TEXT NOT NULL,
            reason TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_stats (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            total_scans INTEGER DEFAULT 0,
            phishing_detected INTEGER DEFAULT 0,
            legitimate_detected INTEGER DEFAULT 0,
            last_updated TEXT
        )
    """)

    cursor.execute("SELECT * FROM app_stats WHERE id = 1")
    row = cursor.fetchone()

    if row is None:
        cursor.execute("""
            INSERT INTO app_stats (id, total_scans, phishing_detected, legitimate_detected, last_updated)
            VALUES (1, 0, 0, 0, ?)
        """, (get_current_timestamp(),))

    conn.commit()
    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    init_database()
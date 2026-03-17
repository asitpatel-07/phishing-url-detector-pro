import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import get_db_connection


def normalize_url_for_block(url: str) -> str:
    return url.strip().lower()


def block_url_for_24_hours(url: str, risk_score: int, reason: str = "High phishing risk"):
    conn = get_db_connection()
    cursor = conn.cursor()

    normalized_url = normalize_url_for_block(url)
    blocked_at = datetime.now()
    blocked_until = blocked_at + timedelta(hours=4)

    cursor.execute("""
        INSERT OR REPLACE INTO blocked_urls (url, risk_score, blocked_at, blocked_until, reason)
        VALUES (?, ?, ?, ?, ?)
    """, (
        normalized_url,
        risk_score,
        blocked_at.strftime("%Y-%m-%d %H:%M:%S"),
        blocked_until.strftime("%Y-%m-%d %H:%M:%S"),
        reason
    ))

    conn.commit()
    conn.close()


def is_url_currently_blocked(url: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    normalized_url = normalize_url_for_block(url)

    cursor.execute("""
        SELECT * FROM blocked_urls WHERE url = ?
    """, (normalized_url,))
    row = cursor.fetchone()

    conn.close()

    if not row:
        return False, None

    blocked_until = datetime.strptime(row["blocked_until"], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()

    if now < blocked_until:
        return True, row["blocked_until"]

    return False, None


def remove_expired_blocks():
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        DELETE FROM blocked_urls
        WHERE blocked_until < ?
    """, (now,))

    conn.commit()
    conn.close()
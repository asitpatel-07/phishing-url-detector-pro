from src.utils import get_db_connection, get_current_timestamp


def normalize_for_blacklist(url):
    return url.strip().lower()


def add_url_to_blacklist(url, source="manual"):
    conn = get_db_connection()
    cursor = conn.cursor()

    normalized_url = normalize_for_blacklist(url)

    try:
        cursor.execute("""
            INSERT INTO blacklist_urls (url, source, added_at)
            VALUES (?, ?, ?)
        """, (normalized_url, source, get_current_timestamp()))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def is_url_blacklisted(url):
    conn = get_db_connection()
    cursor = conn.cursor()

    normalized_url = normalize_for_blacklist(url)

    cursor.execute("""
        SELECT * FROM blacklist_urls WHERE url = ?
    """, (normalized_url,))
    row = cursor.fetchone()

    conn.close()
    return row is not None


def get_all_blacklisted_urls():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM blacklist_urls ORDER BY id DESC
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows


if __name__ == "__main__":
    test_url = input("Enter URL to add to blacklist: ").strip()
    added = add_url_to_blacklist(test_url)
    print("Added:", added)
    print("Is blacklisted:", is_url_blacklisted(test_url))
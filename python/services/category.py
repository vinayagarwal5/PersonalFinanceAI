from services.database import get_connection


def get_category(merchant):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category
        FROM merchant_categories
        WHERE merchant=?
    """, (merchant,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def save_category(merchant, category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR REPLACE INTO merchant_categories

    VALUES
    (?, ?, NULL, CURRENT_TIMESTAMP)

    """, (merchant, category))

    conn.commit()
    conn.close()
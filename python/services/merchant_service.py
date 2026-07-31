from services.database import get_connection
from utils.merchant_rules import MERCHANT_RULES

def get_normalized_merchant(name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT normalized_name

        FROM merchant_master

        WHERE merchant_name=?

    """, (name,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def save_merchant(
        merchant,
        normalized,
        category=None,
        sub_category=None,
        merchant_type=None
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR REPLACE INTO merchant_master

    VALUES
    (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)

    """, (
        merchant,
        normalized,
        category,
        sub_category,
        merchant_type
    ))

    conn.commit()

    conn.close()
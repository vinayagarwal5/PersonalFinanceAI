from services.database import get_connection
from services.merchant_normalizer import get_merchant_details


def refresh_categories():

    conn = get_connection()
    cursor = conn.cursor()

    # Read all transactions
    cursor.execute("""
        SELECT
            id,
            merchant,
            category
        FROM transactions
    """)

    rows = cursor.fetchall()

    total = 0
    updated = 0

    for txn_id, merchant, category in rows:
        total += 1

        details = get_merchant_details(merchant)

        new_merchant = details["merchant"]
        new_category = details["category"]

        # Update only if something has changed
        if merchant != new_merchant or category != new_category:
            cursor.execute(
                """
                UPDATE transactions
                SET
                    merchant=?,
                    category=?
                WHERE id=?
            """,
                (new_merchant, new_category, txn_id),
            )

            updated += 1

    conn.commit()
    conn.close()

    print("=" * 60)
    print("CATEGORY REFRESH COMPLETED")
    print("=" * 60)
    print(f"Total Transactions : {total}")
    print(f"Updated            : {updated}")
    print(f"Unchanged          : {total - updated}")
    print("=" * 60)


if __name__ == "__main__":
    refresh_categories()

from services.database import get_connection


def get_uncategorized_merchants():

    conn = get_connection()

    query = """
    SELECT
        merchant,
        COUNT(*) AS transactions,
        ROUND(SUM(amount),2) AS spending

    FROM transactions

    WHERE
        transaction_type='Debit'
        AND (
            category IS NULL
            OR category=''
            OR category='Others'
        )

    GROUP BY merchant

    ORDER BY spending DESC
    """

    rows = conn.execute(query).fetchall()

    conn.close()

    return rows


def update_category(merchant, category):

    conn = get_connection()

    conn.execute(
        """
        UPDATE transactions
        SET category=?
        WHERE merchant=?
        """,
        (category, merchant),
    )

    conn.commit()

    conn.close()


def main():

    merchants = get_uncategorized_merchants()

    print("=" * 70)
    print("UNCATEGORIZED MERCHANT REVIEW")
    print("=" * 70)

    categories = {
        "1": "Food",
        "2": "Groceries",
        "3": "Fuel",
        "4": "Shopping",
        "5": "Travel",
        "6": "Medical",
        "7": "Education",
        "8": "Utilities",
        "9": "Transfer",
        "10": "Investment",
        "11": "Family",
        "12": "Entertainment",
        "13": "Skip",
    }

    for merchant, count, amount in merchants:
        print("\n" + "-" * 60)

        print(f"Merchant      : {merchant}")
        print(f"Transactions  : {count}")
        print(f"Total Spend   : ₹{amount:,.2f}")

        print("\nChoose Category")

        for key, value in categories.items():
            print(f"{key}. {value}")

        choice = input("\nChoice : ").strip()

        if choice == "13":
            continue

        if choice in categories:
            update_category(merchant, categories[choice])

            print("Updated.")

        else:
            print("Invalid choice.")

    print("\nDone.")


if __name__ == "__main__":
    main()

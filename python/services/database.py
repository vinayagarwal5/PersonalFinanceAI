import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "database" / "finance.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def insert_transaction(transaction):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT OR IGNORE INTO transactions (

            transaction_date,
            transaction_time,

            month,
            financial_year,

            merchant,
            description,

            amount,

            transaction_type,
            payment_mode,

            source,
            account,

            reference_no,

            category,

            raw_text

        )

        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """, (

            transaction["transaction_date"],
            transaction["transaction_time"],

            transaction["month"],
            transaction["financial_year"],

            transaction["merchant"],
            transaction["description"],

            transaction["amount"],

            transaction["transaction_type"],
            transaction["payment_mode"],

            transaction["source"],
            transaction["account"],

            transaction["reference_no"],

            transaction["category"],

            transaction["raw_text"]

        ))

        conn.commit()

        return cursor.rowcount > 0

    finally:
        conn.close()


def get_transaction_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")

    count = cursor.fetchone()[0]

    conn.close()

    return count


def transaction_exists(source, reference_no):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM transactions

        WHERE source=?

        AND reference_no=?

    """, (source, reference_no))

    exists = cursor.fetchone()[0] > 0

    conn.close()

    return exists


def add_processed_file(file_name, file_hash, source):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR IGNORE INTO ingested_files

    (
        file_name,
        file_hash,
        source
    )

    VALUES (?,?,?)

    """, (file_name, file_hash, source))

    conn.commit()

    conn.close()


def file_already_processed(file_hash):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT COUNT(*)

    FROM ingested_files

    WHERE file_hash=?

    """, (file_hash,))

    exists = cursor.fetchone()[0] > 0

    conn.close()

    return exists

def update_category(transaction_id, category):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE transactions

        SET category=?

        WHERE id=?

    """, (category, transaction_id))

    conn.commit()

    conn.close()
def get_all_merchants():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT merchant
        FROM transactions
    """)

    merchants = [row[0] for row in cursor.fetchall()]

    conn.close()

    return merchants


def update_merchant(old_name, new_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET merchant = ?
        WHERE merchant = ?
    """, (new_name, old_name))

    conn.commit()

    conn.close()

def get_uncategorized_transactions():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT id, merchant

    FROM transactions

    WHERE category IS NULL

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
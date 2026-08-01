import sys
from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.database import get_connection


def column_exists(cursor, table_name, column_name):

    cursor.execute(f"PRAGMA table_info({table_name})")

    columns = [row[1] for row in cursor.fetchall()]

    return column_name in columns


def migrate():

    conn = get_connection()
    cursor = conn.cursor()

    print("=" * 60)
    print("Updating merchant_master table...")
    print("=" * 60)

    if not column_exists(cursor, "merchant_master", "is_active"):
        cursor.execute("""
            ALTER TABLE merchant_master
            ADD COLUMN is_active INTEGER DEFAULT 1
        """)

        print("Added column : is_active")

    else:
        print("Column already exists : is_active")

    if not column_exists(cursor, "merchant_master", "last_updated"):
        cursor.execute("""
            ALTER TABLE merchant_master
            ADD COLUMN last_updated TIMESTAMP
        """)
        cursor.execute("""
            UPDATE merchant_master
            SET last_updated = CURRENT_TIMESTAMP
            WHERE last_updated IS NULL
        """)

        print("Added column : last_updated")

    else:
        print("Column already exists : last_updated")

    conn.commit()
    conn.close()

    print("=" * 60)
    print("Merchant Master Updated Successfully")
    print("=" * 60)


if __name__ == "__main__":
    migrate()

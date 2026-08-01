try:
    from ..services.database import get_connection
    from ..utils.merchant_rules import MERCHANT_RULES
except Exception:
    # Support running this migration directly
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from services.database import get_connection
    from utils.merchant_rules import MERCHANT_RULES

import sqlite3


def migrate():

    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    # Detect existing columns in merchant_master
    cursor.execute("PRAGMA table_info(merchant_master)")
    cols = [row[1] for row in cursor.fetchall()]

    if 'merchant_name' in cols:
        key_col = 'merchant_name'
    elif 'keyword' in cols:
        # Standardize to merchant_name, copying existing keyword values
        cursor.execute("ALTER TABLE merchant_master ADD COLUMN merchant_name TEXT")
        cursor.execute("UPDATE merchant_master SET merchant_name = keyword")
        conn.commit()
        key_col = 'merchant_name'
    else:
        cursor.execute("ALTER TABLE merchant_master ADD COLUMN merchant_name TEXT")
        conn.commit()
        key_col = 'merchant_name'

    for keyword, value in MERCHANT_RULES.items():
        # Supports both:
        # "AMAZON": ("Amazon", "Shopping")
        # and future extensions with more fields
        normalized = value[0]
        category = value[1]

        try:
            cursor.execute(f"""
                INSERT OR IGNORE INTO merchant_master
                ({key_col}, normalized_name, category)
                VALUES (?, ?, ?)
            """, (keyword, normalized, category))

            # cursor.rowcount may be 0 if ignored
            if cursor.rowcount and cursor.rowcount > 0:
                inserted += 1

        except sqlite3.IntegrityError as e:
            skipped += 1
            print(f"Skipped [{keyword}] -> {e}")

        except Exception as e:
            print(f"Error [{keyword}] -> {e}")

    conn.commit()
    conn.close()

    print("=" * 60)
    print("MERCHANT RULES MIGRATION")
    print("=" * 60)
    print(f"Rules Found : {len(MERCHANT_RULES)}")
    print(f"Inserted    : {inserted}")
    print(f"Skipped     : {skipped}")
    print("=" * 60)


if __name__ == "__main__":
    migrate()

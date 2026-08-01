try:
    from services.database import get_connection
except Exception:
    # Support running this script directly (not as a package)
    import sys
    from pathlib import Path

    # Add the 'python' package directory to sys.path so 'services' can be imported
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from services.database import get_connection


def create_merchant_master():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS merchant_master (

        merchant_name TEXT PRIMARY KEY,

        normalized_name TEXT NOT NULL,

        category TEXT,

        sub_category TEXT,

        merchant_type TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        is_active INTEGER DEFAULT 1,

        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

    print("=" * 60)
    print("Merchant Master table created successfully")
    print("=" * 60)


if __name__ == "__main__":
    create_merchant_master()

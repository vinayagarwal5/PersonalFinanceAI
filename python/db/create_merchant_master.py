from services.database import get_connection  # type: ignore[import]


def create_merchant_master():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS merchant_master (

        keyword TEXT PRIMARY KEY,

        normalized_name TEXT NOT NULL,

        category TEXT NOT NULL,

        merchant_type TEXT,

        notes TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

    print("=" * 60)
    print("Merchant Master table created successfully")
    print("=" * 60)


if __name__ == "__main__":
    create_merchant_master()

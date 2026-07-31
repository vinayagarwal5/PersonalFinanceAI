from ..python.services.database import get_connection

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

print("=" * 50)
print("Merchant Master table created successfully")
print("=" * 50)
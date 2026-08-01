import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "finance.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    transaction_date TEXT NOT NULL,
    transaction_time TEXT,

    month TEXT NOT NULL,
    financial_year TEXT NOT NULL,

    merchant TEXT NOT NULL,
    description TEXT,

    amount REAL NOT NULL,

    transaction_type TEXT,
    payment_mode TEXT,

    source TEXT NOT NULL,
    account TEXT,

    reference_no TEXT,

    category TEXT,

    raw_text TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(source, reference_no)

);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS ingested_files (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_name TEXT,
    file_hash TEXT UNIQUE,

    source TEXT,

    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
""")

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

);

""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS merchant_categories (

    merchant TEXT PRIMARY KEY,

    category TEXT NOT NULL,

    sub_category TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
""")

cursor.executescript("""

CREATE INDEX IF NOT EXISTS idx_transaction_date
ON transactions(transaction_date);

CREATE INDEX IF NOT EXISTS idx_month
ON transactions(month);

CREATE INDEX IF NOT EXISTS idx_merchant
ON transactions(merchant);

CREATE INDEX IF NOT EXISTS idx_category
ON transactions(category);

CREATE INDEX IF NOT EXISTS idx_source
ON transactions(source);

CREATE INDEX IF NOT EXISTS idx_reference
ON transactions(reference_no);

""")

conn.commit()
conn.close()

print("Database created successfully.")
import os
import sys

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from services.database import get_connection

print("=" * 60)
print("CREATE BUDGET TABLE")
print("=" * 60)

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS budgets (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    month TEXT NOT NULL,

    category TEXT NOT NULL,

    budget_amount REAL NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(month, category)

)
""")

conn.commit()

print("✓ budgets table created successfully")

conn.close()

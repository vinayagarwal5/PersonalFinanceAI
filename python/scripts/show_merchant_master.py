import sys
from pathlib import Path
# Ensure the project 'python' package directory is on sys.path when running directly
sys.path.append(str(Path(__file__).resolve().parent.parent))
from services.database import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("PRAGMA table_info(merchant_master)")
print('Schema:')
for row in cur.fetchall():
    print(row)

print('\nSample rows:')
cur.execute('SELECT * FROM merchant_master LIMIT 10')
cols = [d[0] for d in cur.description]
print(cols)
for r in cur.fetchall():
    print(r)
conn.close()

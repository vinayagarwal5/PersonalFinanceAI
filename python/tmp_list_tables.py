from services.database import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""")

print("=" * 60)
print("DATABASE TABLES")
print("=" * 60)

for row in cursor.fetchall():
    print(row[0])

conn.close()

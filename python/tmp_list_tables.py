from services.database import get_connection; 
conn=get_connection(); 
cur=conn.cursor(); 
cur.execute('PRAGMA table_info(merchant_master)'); 
[print(row) for row in cur.fetchall()]; conn.close()
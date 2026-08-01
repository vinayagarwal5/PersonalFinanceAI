from services.database import get_connection; 
conn=get_connection();
cur=conn.cursor(); 
cur.execute('SELECT COUNT(*) FROM merchant_master'); 
print(cur.fetchone()[0]); conn.close()
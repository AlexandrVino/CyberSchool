import sqlite3


conn = sqlite3.connect('../../static/database/db.db')
cur = conn.cursor()

#Create certificates table and fill data
cur.execute("""CREATE TABLE IF NOT EXISTS certificates(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   index_number INT,
   number_certificate TEXT,
   product_name TEXT, 
   product_type TEXT,
   order_number INT,
   consumer_organization TEXT,
   shop_manufacturer TEXT,
   full_name_of_the_certificate_issuer TEXT
   );
""")


conn.commit()
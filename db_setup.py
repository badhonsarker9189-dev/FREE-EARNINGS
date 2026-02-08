import sqlite3

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
(id INTEGER PRIMARY KEY, name TEXT, balance REAL, referrer INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS tasks
(id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, status TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS withdraws
(id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, method TEXT, account TEXT, status TEXT)''')

conn.commit()
conn.close()
print("Database created ✅")

import sqlite3
db = r'C:\Users\Administrator\AppData\Roaming\QClaw\qclaw.db'
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print('--- tables ---')
for r in cur.fetchall(): print(r[0])

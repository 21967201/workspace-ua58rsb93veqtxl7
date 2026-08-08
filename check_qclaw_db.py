import sqlite3, os

path = r"C:\Users\Administrator\AppData\Roaming\QClaw\qclaw.db"
print(f"=== {path} ===")
print(f"大小: {os.path.getsize(path)} bytes")
conn = sqlite3.connect(path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print(f"表: {tables}")
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM '{t}'")
        print(f"  {t}: {cur.fetchone()[0]} 行")
    except Exception as e:
        print(f"  {t}: {e}")
conn.close()

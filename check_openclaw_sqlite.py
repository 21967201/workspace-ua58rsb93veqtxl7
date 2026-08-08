import sqlite3, os, datetime

path = r"C:\Users\Administrator\.qclaw\state\openclaw.sqlite"
print(f"=== {path} ===")
print(f"大小: {os.path.getsize(path)} bytes")
print(f"修改: {datetime.datetime.fromtimestamp(os.path.getmtime(path))}")
conn = sqlite3.connect(path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print(f"表 ({len(tables)}): {tables}")
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM '{t}'")
        print(f"  {t}: {cur.fetchone()[0]} 行")
    except Exception as e:
        print(f"  {t}: {e}")
conn.close()

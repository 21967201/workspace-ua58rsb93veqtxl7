import sqlite3, os, datetime

path = r"C:\Users\Administrator\.hermes\profiles\qclawx\state.db"
print(f"=== {path} ===")
print(f"大小: {os.path.getsize(path)} bytes")
print(f"修改时间: {datetime.datetime.fromtimestamp(os.path.getmtime(path))}")
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

# sessions 表详情
try:
    cur.execute("SELECT * FROM sessions ORDER BY rowid DESC LIMIT 10")
    rows = cur.fetchall()
    print(f"\n=== sessions 最新 10 条 ===")
    cols = [d[0] for d in cur.description]
    for r in rows:
        d = dict(zip(cols, r))
        print(f"  id={d.get('id')} | source={d.get('source')} | model={d.get('model')} | title={str(d.get('title'))[:40]} | msg_count={d.get('message_count')} | created={d.get('created_at')} | updated={d.get('updated_at')}")
except Exception as e:
    print(f"sessions 查询失败: {e}")

# messages 表
try:
    cur.execute("SELECT COUNT(*) FROM messages")
    print(f"\nmessages 总数: {cur.fetchone()[0]}")
    cur.execute("SELECT id, role, substr(content,1,80) as c, created_at FROM messages ORDER BY rowid DESC LIMIT 10")
    print("=== messages 最新 10 条 ===")
    for r in cur.fetchall():
        print(f"  {r['id']} | {r['role']} | {r['c']} | {r['created_at']}")
except Exception as e:
    print(f"messages 查询失败: {e}")
conn.close()

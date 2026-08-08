import sqlite3, os, datetime

# 检查 .qclaw-hermes/state.db 的会话时间分布
p = r'C:\Users\Administrator\.qclaw-hermes\state.db'
conn = sqlite3.connect(p)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("=== state.db 表 ===")
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print([r[0] for r in cur.fetchall()])

# sessions 结构
cur.execute("PRAGMA table_info(sessions)")
cols = [r['name'] for r in cur.fetchall()]
print(f"\nsessions 列: {cols}")

# 按日期统计
cur.execute("SELECT substr(started_at,1,10) as d, COUNT(*) FROM sessions GROUP BY d ORDER BY d")
print("\n=== sessions 按日期 ===")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")

# 老会话的消息数
print("\n=== 老会话 (6月) 消息统计 ===")
cur.execute("SELECT s.id, s.title, COUNT(m.id) as mc FROM sessions s LEFT JOIN messages m ON m.session_id = s.id WHERE s.started_at LIKE '202606%' GROUP BY s.id ORDER BY s.started_at DESC LIMIT 15")
for r in cur.fetchall():
    print(f"  {r['id']} | title={str(r['title'])[:30]} | {r['mc']} msgs")

# messages 表结构
cur.execute("PRAGMA table_info(messages)")
print(f"\nmessages 列: {[r['name'] for r in cur.fetchall()]}")
conn.close()

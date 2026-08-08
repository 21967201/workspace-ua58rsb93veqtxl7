import sqlite3, os, datetime

p = r'C:\Users\Administrator\.qclaw-hermes\state.db'
conn = sqlite3.connect(p)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def ts2str(ts):
    try:
        return datetime.datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M')
    except:
        return str(ts)

# 日期分布
cur.execute("SELECT started_at, COUNT(*) as c FROM sessions GROUP BY CAST(started_at/86400 AS INT) ORDER BY started_at")
print("=== sessions 按天分布 ===")
for r in cur.fetchall():
    print(f"  {ts2str(r['started_at'])}: {r['c']}")

# 消息总数
cur.execute("SELECT COUNT(*) FROM messages")
print(f"\nmessages 总数: {cur.fetchone()[0]}")

# 各会话消息数（Top 20）
cur.execute("""
    SELECT s.id, s.title, s.started_at, COUNT(m.id) as mc
    FROM sessions s LEFT JOIN messages m ON m.session_id = s.id
    GROUP BY s.id ORDER BY s.started_at DESC LIMIT 30
""")
print("\n=== 最新 30 会话及其消息数 ===")
for r in cur.fetchall():
    print(f"  {r['id']} | {ts2str(r['started_at'])} | {r['mc']} msgs | {str(r['title'])[:35]}")

# 6月会话消息数
print("\n=== 6月会话消息数（时间戳 < 1783000000）===")
cur.execute("""
    SELECT s.id, s.title, s.started_at, COUNT(m.id) as mc
    FROM sessions s LEFT JOIN messages m ON m.session_id = s.id
    WHERE s.started_at < 1783000000
    GROUP BY s.id ORDER BY s.started_at
""")
rows = cur.fetchall()
print(f"共 {len(rows)} 个老会话")
total = sum(r['mc'] for r in rows)
print(f"总消息数: {total}")
for r in rows[:20]:
    print(f"  {r['id']} | {ts2str(r['started_at'])} | {r['mc']} msgs | {str(r['title'])[:40]}")
conn.close()

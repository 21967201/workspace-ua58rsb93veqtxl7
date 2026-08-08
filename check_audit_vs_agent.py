import sqlite3, datetime

path = r"C:\Users\Administrator\.qclaw-hermes\audit.db"
conn = sqlite3.connect(path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# 转时间戳
def ts2str(ts):
    try:
        return datetime.datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ts)

print("=== audit_messages 时间范围 ===")
cur.execute("SELECT MIN(timestamp), MAX(timestamp), COUNT(*) FROM audit_messages")
r = cur.fetchone()
print(f"最早: {ts2str(r[0])} | 最晚: {ts2str(r[1])} | 总数: {r[2]}")

print("\n=== 最新 8 个会话的消息统计 ===")
cur.execute("SELECT session_id, COUNT(*) as cnt, MIN(timestamp) as mn, MAX(timestamp) as mx FROM audit_messages GROUP BY session_id ORDER BY mx DESC LIMIT 10")
for r in cur.fetchall():
    print(f"  {r['session_id']} | {r['cnt']} msgs | {ts2str(r['mn'])} → {ts2str(r['mx'])}")

print("\n=== 关键会话 20260808_095320_43ecf0（agent.json 第一个）===")
cur.execute("SELECT session_id, COUNT(*) FROM audit_messages WHERE session_id LIKE '20260808%' GROUP BY session_id")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]} msgs")
cur.execute("SELECT COUNT(*) FROM audit_messages WHERE session_id='20260808_095320_43ecf0'")
print(f"  095320_43ecf0: {cur.fetchone()[0]} msgs")

print("\n=== agent.json 提到但 audit.db 没有的 session ===")
# 从 agent.json 读 sessionIds
import json
with open(r"C:\Users\Administrator\.qclaw-hermes\agent.json", encoding='utf-8') as f:
    agent = json.load(f)
sids = agent.get('sessionIds', [])
print(f"agent.json sessionIds 总数: {len(sids)}")
cur.execute("SELECT DISTINCT session_id FROM audit_messages")
db_sids = set(r[0] for r in cur.fetchall())
missing = [s for s in sids if s not in db_sids and not s.startswith('cron_')]
print(f"audit.db 中缺失的 (非cron): {len(missing)}")
for m in missing[:20]:
    print(f"  {m}")
conn.close()

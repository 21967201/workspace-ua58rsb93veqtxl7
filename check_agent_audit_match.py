import sqlite3, json, os

QH = r'C:\Users\Administrator\.qclaw-hermes'

# 1. agent.json 当前 sessionIds
agent = json.load(open(os.path.join(QH, 'agent.json'), encoding='utf-8'))
sids = agent.get('sessionIds', [])
print(f"agent.json: {len(sids)} sessionIds")

# 2. audit.db 会话
audit = sqlite3.connect(os.path.join(QH, 'audit.db'))
cur = audit.cursor()
cur.execute("SELECT DISTINCT session_id FROM audit_messages")
db_sids = set(r[0] for r in cur.fetchall())
print(f"audit.db: {len(db_sids)} 会话有消息")

# 3. state.db 会话
state = sqlite3.connect(os.path.join(QH, 'state.db'))
scur = state.cursor()
scur.execute("SELECT id FROM sessions")
state_sids = set(r[0] for r in scur.fetchall())
print(f"state.db: {len(state_sids)} 会话")

sid_set = set(sids)
print(f"\nagent.json 有但 audit.db 没有 ({len(sid_set - db_sids)}):")
for s in sorted(sid_set - db_sids)[:20]:
    print(f"  {s}")

print(f"\naudit.db 有但 agent.json 没有 ({len(db_sids - sid_set)}):")
for s in sorted(db_sids - sid_set)[:20]:
    print(f"  {s}")

# 4. agent.json 的 titles 数
titles = agent.get('sessionTitles', {})
print(f"\nagent.json sessionTitles: {len(titles)}")

# 5. 是否有 sessionUpdatedAts
sua = agent.get('sessionUpdatedAts', {})
print(f"agent.json sessionUpdatedAts: {len(sua)}")

audit.close()
state.close()

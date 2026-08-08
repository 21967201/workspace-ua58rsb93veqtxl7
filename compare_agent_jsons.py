import json, os

base = r'C:\Users\Administrator\.qclaw-hermes'
variants = {
    'current': os.path.join(base, 'agent.json'),
    'postmerge': os.path.join(base, 'state-merge-backup', 'agent.json.postmerge'),
    'cleanup': os.path.join(base, 'state-merge-backup', 'agent.json.cleanup.103842'),
    'polluted': os.path.join(base, 'state-merge-backup', 'agent.json.polluted.111315'),
}

all_sids = {}
for name, path in variants.items():
    if not os.path.exists(path):
        print(f"{name}: 不存在")
        continue
    d = json.load(open(path, encoding='utf-8'))
    sids = d.get('sessionIds', [])
    all_sids[name] = set(sids)
    print(f"{name}: {len(sids)} sessionIds")

print("\n=== 差异分析 ===")
cur = all_sids.get('current', set())
post = all_sids.get('postmerge', set())
clean = all_sids.get('cleanup', set())
poll = all_sids.get('polluted', set())

print(f"\npostmerge 有但 current 没有 ({len(post - cur)}):")
for s in sorted(post - cur):
    print(f"  {s}")

print(f"\ncurrent 有但 postmerge 没有 ({len(cur - post)}):")
for s in sorted(cur - post):
    print(f"  {s}")

print(f"\ncurrent 有但 cleanup 没有 ({len(cur - clean)}):")
for s in sorted(cur - clean):
    print(f"  {s}")

# 检查 audit.db 覆盖情况
import sqlite3
conn = sqlite3.connect(os.path.join(base, 'audit.db'))
cur_db = conn.cursor()
cur_db.execute("SELECT DISTINCT session_id FROM audit_messages")
db_sids = set(r[0] for r in cur_db.fetchall())
print(f"\naudit.db 有消息的 session_id 数: {len(db_sids)}")

print(f"\npostmerge 会话中 audit.db 无消息的 ({len(post - db_sids)}):")
for s in sorted(post - db_sids)[:30]:
    print(f"  {s}")
conn.close()

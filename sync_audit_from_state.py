import sqlite3

# audit.db 结构
print("=== audit.db 表结构 ===")
audit = sqlite3.connect(r'C:\Users\Administrator\.qclaw-hermes\audit.db')
a_cur = audit.cursor()
a_cur.execute("PRAGMA table_info(audit_messages)")
for r in a_cur.fetchall():
    print(f"  audit_messages: {r[1]} {r[2]} notnull={r[3]}")

a_cur.execute("PRAGMA table_info(conversation_sessions)")
for r in a_cur.fetchall():
    print(f"  conversation_sessions: {r[1]} {r[2]} notnull={r[3]}")

# state.db 结构
print("\n=== state.db messages 表结构 ===")
state = sqlite3.connect(r'C:\Users\Administrator\.qclaw-hermes\state.db')
s_cur = state.cursor()
s_cur.execute("PRAGMA table_info(messages)")
for r in s_cur.fetchall():
    print(f"  messages: {r[1]} {r[2]} notnull={r[3]}")

# 抽样对比
a_cur.execute("SELECT * FROM audit_messages ORDER BY rowid DESC LIMIT 1")
a_row = dict(zip([d[0] for d in a_cur.description], a_cur.fetchone()))
print(f"\naudit 样本: {str(a_row)[:300]}")

s_cur.execute("SELECT * FROM messages ORDER BY rowid DESC LIMIT 1")
s_row = dict(zip([d[0] for d in s_cur.description], s_cur.fetchone()))
print(f"state 样本: {str(s_row)[:300]}")

# 覆盖计算
a_cur.execute("SELECT DISTINCT session_id FROM audit_messages")
a_sessions = set(r[0] for r in a_cur.fetchall())
s_cur.execute("SELECT DISTINCT id FROM sessions")
s_sessions = set(r[0] for r in s_cur.fetchall())
missing = s_sessions - a_sessions
print(f"\nstate.db 会话: {len(s_sessions)} | audit.db 覆盖: {len(a_sessions)} | 缺失: {len(missing)}")

s_cur.execute("""
    SELECT s.id, s.title, s.started_at, COUNT(m.id) as mc
    FROM sessions s LEFT JOIN messages m ON m.session_id = s.id
    WHERE s.id IN ({})
    GROUP BY s.id ORDER BY s.started_at
""".format(','.join('?'*len(missing))), list(missing))
total = 0
for r in s_cur.fetchall():
    print(f"  {r[0]} | {r[2]} | {r[3]} msgs | {str(r[1])[:40]}")
    total += r[3]
print(f"\n缺失消息总数: {total}")

audit.close()
state.close()

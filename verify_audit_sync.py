import sqlite3, datetime

audit = sqlite3.connect(r'C:\Users\Administrator\.qclaw-hermes\audit.db')
a_cur = audit.cursor()

# 验证关键老会话
print("=== 关键老会话消息验证 ===")
checks = [
    ('20260618_150616_fda3e8', 'Kermes与OfficeClaw双Agent协作'),
    ('20260618_155645_1ba683', 'HermesX Workspace Configuration'),
    ('20260626_175130_c7bef6', 'Agent差异化进化优化方案'),
    ('20260627_181934_7b9ae4', 'WorkBuddyX项目学习'),
    ('20260629_181323_48b61f', 'Hermes Agent v0.17.0'),
    ('20260630_173827_577ee9', '今日头条AI Agent趋势'),
    ('20260805_165324_cc5baa', '8/5 会话'),
]
for sid, label in checks:
    a_cur.execute("SELECT COUNT(*) FROM audit_messages WHERE session_id = ?", (sid,))
    c = a_cur.fetchone()[0]
    print(f"  {label}: {c} 消息")

# 按日期分布
print("\n=== audit_messages 按会话日期分布 ===")
a_cur.execute("""
    SELECT substr(session_id, 1, 8) as d, COUNT(DISTINCT session_id) as sc, COUNT(*) as mc
    FROM audit_messages GROUP BY d ORDER BY d
""")
for r in a_cur.fetchall():
    print(f"  {r[0]}: {r[1]} 会话, {r[2]} 消息")

# 最新消息时间
a_cur.execute("SELECT MAX(timestamp) FROM audit_messages")
maxts = a_cur.fetchone()[0]
print(f"\n最新消息时间: {datetime.datetime.fromtimestamp(maxts)}")

# event_type 分布
a_cur.execute("SELECT event_type, COUNT(*) FROM audit_messages GROUP BY event_type")
print("\nevent_type 分布:")
for r in a_cur.fetchall():
    print(f"  {r[0]}: {r[1]}")
audit.close()

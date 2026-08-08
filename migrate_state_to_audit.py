"""
将 .qclaw-hermes/state.db 中缺失的会话消息同步到 audit.db
安全步骤：
1. 备份 audit.db
2. 按会话逐批迁移（幂等，跳过已存在会话）
3. 写 conversation_sessions 映射
4. 验证
"""
import sqlite3, os, shutil, datetime, sys

QH = r'C:\Users\Administrator\.qclaw-hermes'
AUDIT = os.path.join(QH, 'audit.db')
STATE = os.path.join(QH, 'state.db')

# 1. 备份
backup = os.path.join(QH, f'audit.db.bak-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}')
if os.path.exists(AUDIT):
    # 用 SQLite backup API 而非文件拷贝（避免 WAL 问题）
    src = sqlite3.connect(AUDIT)
    dst = sqlite3.connect(backup)
    src.backup(dst)
    dst.close()
    src.close()
    print(f"✅ 备份 audit.db → {backup} ({os.path.getsize(backup)} bytes)")
else:
    print(f"❌ audit.db 不存在: {AUDIT}")
    sys.exit(1)

audit = sqlite3.connect(AUDIT)
state = sqlite3.connect(STATE)
audit.row_factory = sqlite3.Row
state.row_factory = sqlite3.Row
a_cur = audit.cursor()
s_cur = state.cursor()

# 2. 确定缺失会话
a_cur.execute("SELECT DISTINCT session_id FROM audit_messages")
existing = set(r[0] for r in a_cur.fetchall())
s_cur.execute("SELECT id FROM sessions")
all_state = set(r[0] for r in s_cur.fetchall())
missing = sorted(all_state - existing)
print(f"需要迁移: {len(missing)} 个会话")

# 3. 逐会话迁移
migrated_sessions = 0
migrated_msgs = 0
for sid in missing:
    s_cur.execute("""
        SELECT id, session_id, role, content, tool_call_id, tool_calls, tool_name,
               timestamp, reasoning, reasoning_content
        FROM messages WHERE session_id = ?
        ORDER BY timestamp, id
    """, (sid,))
    msgs = s_cur.fetchall()
    if not msgs:
        # 空会话也注册 conversation_sessions（如果 state.db sessions 表里有）
        s_cur.execute("SELECT id, title FROM sessions WHERE id = ?", (sid,))
        srow = s_cur.fetchone()
        if srow:
            a_cur.execute(
                "INSERT OR IGNORE INTO conversation_sessions (conversation_name, session_id, root_session_id, created_at) VALUES (?,?,?,?)",
                (f"migrated-{sid}", sid, sid, srow['id'] and 0 or 0)
            )
        continue
    root_sid = sid  # 会话 id 即 root
    for m in msgs:
        a_cur.execute("""
            INSERT INTO audit_messages
            (session_id, root_session_id, role, content, tool_call_id, tool_calls, tool_name,
             timestamp, reasoning, reasoning_content, model, event_type)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            m['session_id'] or sid, root_sid, m['role'], m['content'],
            m['tool_call_id'], m['tool_calls'], m['tool_name'],
            m['timestamp'], m['reasoning'], m['reasoning_content'], None,
            'migrated'
        ))
        migrated_msgs += 1
    # conversation_sessions 映射
    a_cur.execute(
        "INSERT OR IGNORE INTO conversation_sessions (conversation_name, session_id, root_session_id, created_at) VALUES (?,?,?,?)",
        (f"migrated-{sid}", sid, root_sid, m['timestamp'])
    )
    migrated_sessions += 1
    if migrated_sessions % 20 == 0:
        audit.commit()
        print(f"  进度: {migrated_sessions}/{len(missing)} 会话, {migrated_msgs} 消息")

audit.commit()
print(f"\n✅ 迁移完成: {migrated_sessions} 会话, {migrated_msgs} 消息")

# 4. 验证
a_cur.execute("SELECT COUNT(*) FROM audit_messages")
print(f"audit_messages 总数: {a_cur.fetchone()[0]}")
a_cur.execute("SELECT COUNT(DISTINCT session_id) FROM audit_messages")
print(f"audit_messages 会话数: {a_cur.fetchone()[0]}")
a_cur.execute("SELECT COUNT(*) FROM conversation_sessions")
print(f"conversation_sessions 总数: {a_cur.fetchone()[0]}")

audit.close()
state.close()
print("\n🎉 同步完成！前端应能显示全部历史会话。")

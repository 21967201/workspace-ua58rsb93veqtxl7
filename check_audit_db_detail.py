import sqlite3, os, datetime

path = r"C:\Users\Administrator\.qclaw-hermes\audit.db"
conn = sqlite3.connect(path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("=== conversation_sessions 全部 ===")
cur.execute("PRAGMA table_info(conversation_sessions)")
cols = [r['name'] for r in cur.fetchall()]
print(f"列: {cols}")
cur.execute("SELECT * FROM conversation_sessions ORDER BY rowid DESC LIMIT 30")
for r in cur.fetchall():
    d = dict(r)
    print(f"  {str(d)[:220]}")

print("\n=== audit_messages 结构 ===")
cur.execute("PRAGMA table_info(audit_messages)")
cols = [r['name'] for r in cur.fetchall()]
print(f"列: {cols}")
cur.execute("SELECT * FROM audit_messages ORDER BY rowid DESC LIMIT 5")
for r in cur.fetchall():
    d = dict(r)
    print(f"  {str(d)[:250]}")
conn.close()

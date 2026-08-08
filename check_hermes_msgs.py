import sqlite3, json

def show_messages(db_path, label, limit=15):
    print(f"===== {label} messages =====")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(messages)")
        cols = [r["name"] for r in cur.fetchall()]
        print(f"messages 列: {cols}")
        cur.execute("SELECT * FROM messages ORDER BY rowid DESC LIMIT ?", (limit,))
        for r in cur.fetchall():
            d = dict(r)
            brief = {}
            for k, v in d.items():
                if isinstance(v, str) and len(v) > 100:
                    brief[k] = v[:100] + "..."
                elif k == "content" and v is not None:
                    brief[k] = str(v)[:100] + ("..." if len(str(v)) > 100 else "")
                else:
                    brief[k] = v
            print(f"  {json.dumps(brief, ensure_ascii=False, default=str)[:350]}")
    except Exception as e:
        print(f"  错误: {e}")
    print()

show_messages(r"C:\Users\Administrator\.hermes\state.db", "主 state.db")
show_messages(r"C:\Users\Administrator\.hermes\profiles\qclawx\state.db", "qclawx state.db")

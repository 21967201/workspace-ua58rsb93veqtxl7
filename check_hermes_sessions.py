import sqlite3, os, json

def show_sessions(db_path, label):
    print(f"===== {label} =====")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(sessions)")
        cols = [r["name"] for r in cur.fetchall()]
        print(f"sessions 列: {cols}")
        cur.execute("SELECT * FROM sessions ORDER BY rowid DESC LIMIT 10")
        rows = cur.fetchall()
        for r in rows:
            d = dict(r)
            # 精简显示
            brief = {}
            for k, v in d.items():
                if isinstance(v, str) and len(v) > 80:
                    brief[k] = v[:80] + "..."
                else:
                    brief[k] = v
            print(f"  {json.dumps(brief, ensure_ascii=False, default=str)[:300]}")
    except Exception as e:
        print(f"  sessions 错误: {e}")
    print()

show_sessions(r"C:\Users\Administrator\.hermes\state.db", "主 state.db")
show_sessions(r"C:\Users\Administrator\.hermes\profiles\qclawx\state.db", "qclawx state.db")

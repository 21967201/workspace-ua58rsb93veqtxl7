import sqlite3, os, datetime

paths = [
    r"C:\Users\Administrator\.qclaw-hermes\audit.db",
    r"C:\Users\Administrator\.qclaw-hermes\memory_store.db",
]

for path in paths:
    if not os.path.exists(path):
        print(f"不存在: {path}")
        continue
    size = os.path.getsize(path)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    wal = path + "-wal"
    wal_size = os.path.getsize(wal) if os.path.exists(wal) else 0
    print(f"\n=== {path} ===")
    print(f"大小: {size} bytes ({size/1024/1024:.1f} MB), WAL: {wal_size} bytes")
    print(f"修改: {mtime}")
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        print(f"表 ({len(tables)}):")
        for t in tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM '{t}'")
                print(f"  {t}: {cur.fetchone()[0]} 行")
            except: pass

        # audit.db 里找会话相关
        if 'audit' in path.lower():
            for t in ['audit_events', 'sessions', 'messages', 'conversations']:
                try:
                    cur.execute(f"SELECT * FROM '{t}' ORDER BY rowid DESC LIMIT 3")
                    rows = cur.fetchall()
                    if rows:
                        print(f"\n  [{t}] 最新3条:")
                        for r in rows:
                            d = dict(r)
                            print(f"    {str(d)[:150]}")
                except: pass
        conn.close()
    except Exception as e:
        print(f"错误: {e}")

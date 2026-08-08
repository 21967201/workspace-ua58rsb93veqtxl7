import sqlite3, os, sys

def dump_db(path, label):
    print(f"=== {label}: {path} ===")
    if not os.path.exists(path):
        print("  不存在")
        return
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        print(f"  表: {tables}")
        for t in tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM '{t}'")
                cnt = cur.fetchone()[0]
                print(f"    {t}: {cnt} 行")
            except Exception as e:
                print(f"    {t}: count 失败 {e}")
        conn.close()
    except Exception as e:
        print(f"  错误: {e}")
    print()

dump_db(r"C:\Users\Administrator\.hermes\state.db", "主 state.db")
dump_db(r"C:\Users\Administrator\.hermes\profiles\qclawx\state.db", "qclawx state.db")

# 找所有 sqlite 文件
print("=== .hermes 下所有 .db 文件 ===")
for root, dirs, files in os.walk(r"C:\Users\Administrator\.hermes"):
    for f in files:
        if f.endswith(".db") or f.endswith(".db-wal") or f.endswith(".db-shm"):
            p = os.path.join(root, f)
            sz = os.path.getsize(p)
            print(f"  {p} ({sz} bytes)")

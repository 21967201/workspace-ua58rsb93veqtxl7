import psutil, os

pid = 17440
try:
    p = psutil.Process(pid)
    print("进程:", p.name(), "PID:", pid)
    print("cmdline:", p.cmdline())
    print("cwd:", p.cwd())
    print("\nenviron (HERMES/QCLAW 相关):")
    for k, v in p.environ().items():
        if any(s in k.upper() for s in ["HERMES", "QCLAW", "PYTHON", "VIRTUAL"]):
            print(f"  {k} = {v}")
except Exception as e:
    print("错误:", e)

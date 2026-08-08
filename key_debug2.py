import json, base64, sys
sys.path.insert(0, r"D:\QClaw\v0.2.35.624\resources\hermes\libs")
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

path = r"C:\Users\Administrator\AppData\Roaming\QClaw\logs\hermes\2026-08-08.enc"
with open(path, "rb") as f:
    first_line = f.readline().strip()
    rest = f.read()

meta = json.loads(first_line)
key = base64.b64decode(meta["key"])
print("key 类型:", type(key), "长度:", len(key))
print("AESGCM 实例化...")
aesgcm = AESGCM(key)
print("OK")

lines = [l for l in rest.split(b"\n") if l.strip()]
print("行数:", len(lines))
ok = 0
fail = 0
for i, line in enumerate(lines[:10]):
    try:
        payload = base64.b64decode(line)
        nonce = payload[:12]
        ct = payload[12:]
        pt = aesgcm.decrypt(nonce, ct, None)
        print(f"行{i}: 解密OK len={len(pt)}")
        ok += 1
    except Exception as e:
        print(f"行{i}: 失败 {e}")
        fail += 1
print(f"OK={ok} FAIL={fail}")

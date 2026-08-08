import json, os, base64, sys
sys.path.insert(0, r"D:\QClaw\v0.2.35.624\resources\hermes\libs")
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

path = r"C:\Users\Administrator\AppData\Roaming\QClaw\logs\hermes\2026-08-08.enc"
with open(path, "rb") as f:
    first_line = f.readline().strip()
    rest = f.read()

meta = json.loads(first_line)
key = base64.b64decode(meta["key"])
lines = [l for l in rest.split(b"\n") if l.strip()]
out_lines = []
for line in lines:
    try:
        payload = base64.b64decode(line)
        nonce = payload[:12]
        ct = payload[12:]
        pt = AESGCM(key).decrypt(nonce, ct, None)
        out_lines.append(pt.decode("utf-8", errors="replace"))
    except Exception as e:
        out_lines.append(f"[解密失败: {e}]")

print("=== 前 30 行 ===")
for ln in out_lines[:30]:
    print(ln[:250])
print("\n=== 最后 30 行 ===")
for ln in out_lines[-30:]:
    print(ln[:250])

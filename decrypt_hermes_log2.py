import json, os, base64, sys
sys.path.insert(0, r"D:\QClaw\v0.2.35.624\resources\hermes\libs")
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

path = r"C:\Users\Administrator\AppData\Roaming\QClaw\logs\hermes\2026-08-08.enc"
with open(path, "rb") as f:
    first_line = f.readline().strip()
    rest = f.read()

meta = json.loads(first_line)
key_s = meta["key"]
# key 是 32 字符的 UTF-8 字符串（KZcjTZeOI3vrSBAfumt9lgnoUCl4GS/IX5r9SB2K = 32 字符 = 256bit）
key = key_s.encode("utf-8")
print("key len:", len(key))

# 逐行处理：每行都是 base64(nonce+ciphertext)
lines = [l for l in rest.split(b"\n") if l.strip()]
print("总行数:", len(lines))
out_lines = []
for i, line in enumerate(lines):
    try:
        payload = base64.b64decode(line)
        nonce = payload[:12]
        ct = payload[12:]
        aesgcm = AESGCM(key)
        pt = aesgcm.decrypt(nonce, ct, None)
        out_lines.append(pt.decode("utf-8", errors="replace"))
    except Exception as e:
        out_lines.append(f"[行{i}解密失败: {e}]")

text = "\n".join(out_lines)
print("=== 解密文本总长:", len(text))
# 找错误/会话相关
import re
print("\n=== ERROR/会话相关行 ===")
for ln in out_lines:
    if re.search(r"error|Error|ERROR|session|Session|hermes|Hermes|轩恒|对话|丢失|fail|Fail|empty", ln):
        print(ln[:300])

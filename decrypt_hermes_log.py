import json, os, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def decrypt_enc(path):
    with open(path, "rb") as f:
        header = f.readline().strip()
        meta = json.loads(header)
        key = meta["key"].encode() if isinstance(meta["key"], str) else meta["key"]
        if isinstance(key, str):
            key = base64.b64decode(key) if len(key) > 32 else key.encode()
        alg = meta.get("alg", "aes-256-gcm")
        # read rest
        data = f.read()
    return meta, data

# 尝试解析完整格式：头 + payload
path = r"C:\Users\Administrator\AppData\Roaming\QClaw\logs\hermes\2026-08-08.enc"
with open(path, "rb") as f:
    first_line = f.readline().strip()
    rest = f.read()

meta = json.loads(first_line)
print("meta keys:", list(meta.keys()))
print("meta:", {k: (str(v)[:40]) for k, v in meta.items()})

# 常见格式: {"v":1,"alg":"aes-256-gcm","key":"..."} 后跟 base64(nonce+ciphertext)
key_s = meta.get("key")
try:
    key = base64.b64decode(key_s)
except Exception:
    key = key_s.encode()
print("key len:", len(key))
import base64 as b64
try:
    payload = b64.b64decode(rest)
    print("rest base64 decoded, len:", len(payload))
    # AESGCM: nonce (12) + ciphertext
    nonce = payload[:12]
    ct = payload[12:]
    aesgcm = AESGCM(key)
    pt = aesgcm.decrypt(nonce, ct, None)
    print("解密成功! 前 2000 字符:")
    print(pt[:2000].decode("utf-8", errors="replace"))
except Exception as e:
    print("base64+AESGCM 失败:", e)
    # 尝试: 剩余是 JSON 结构
    try:
        obj = json.loads(rest)
        print("rest 是 JSON:", str(obj)[:500])
    except Exception as e2:
        print("rest 不是 JSON:", e2)
        # 尝试第一行后就是日志文本？
        print("rest 原始前 200:", rest[:200])

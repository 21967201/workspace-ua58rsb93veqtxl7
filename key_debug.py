import json, base64

path = r"C:\Users\Administrator\AppData\Roaming\QClaw\logs\hermes\2026-08-08.enc"
with open(path, "rb") as f:
    first_line = f.readline().strip()

meta = json.loads(first_line)
key_s = meta["key"]
print("key 字符串:", repr(key_s))
print("key 长度:", len(key_s))
b = base64.b64decode(key_s)
print("b64decode 后长度:", len(b))
print("hex:", b.hex())

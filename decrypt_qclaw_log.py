"""解密 QClaw .enc 日志（key 在文件头 JSON 里），使用 hermes libs 的 cryptography"""
import json, base64, sys, os

sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')

def decrypt_enc(path):
    with open(path, 'rb') as f:
        data = f.read()
    nl = data.find(b'\n')
    header = json.loads(data[:nl].decode('utf-8'))
    key = base64.b64decode(header['key'])
    payload = data[nl+1:]
    iv = base64.b64decode(header.get('iv', '')) if header.get('iv') else payload[:12]
    if header.get('iv'):
        tag = payload[-16:]
        ciphertext = payload[:-16]
    else:
        tag = payload[-16:]
        ciphertext = payload[12:-16]
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(iv, ciphertext + tag, None)
    return plaintext.decode('utf-8', errors='replace')

if __name__ == '__main__':
    path = sys.argv[1]
    out = decrypt_enc(path)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    print(out[:n])

"""检查 .enc 文件头结构"""
import json, base64, sys, os

def inspect(path):
    with open(path, 'rb') as f:
        data = f.read()
    nl = data.find(b'\n')
    print(f"文件大小: {len(data)}, 首个换行在: {nl}")
    header_raw = data[:nl]
    print(f"header 原始 ({len(header_raw)} bytes):")
    print(header_raw.decode('utf-8', errors='replace')[:2000])
    header = json.loads(header_raw.decode('utf-8'))
    print(f"\nheader keys: {list(header.keys())}")
    for k, v in header.items():
        if k == 'key':
            print(f"  {k}: len={len(v)}, base64解码后={len(base64.b64decode(v))} bytes")
        else:
            print(f"  {k}: {str(v)[:100]}")
    print(f"\npayload 从 {nl+1} 开始, {len(data)-nl-1} bytes")
    print(f"payload 前 16 bytes hex: {(data[nl+1:nl+17].hex())}")

inspect(sys.argv[1])

import os

# Search for the UTF-8 bytes of "找不到 Hermes CLI 模块" in the entire QClaw directory
# UTF-8: 找=e4 bd a0 不到=b8 b6, 空格=20, H=48 e=65 r=72 m=6d e=65 s=73
# 空格=20, C=43 l=6c i=69, 空格=20, M=4d o=6f d=64, u=75 l=6c e=65 =e6 a8 a1 e5 9d 97=e7 bb=84

needle = "找不到 Hermes CLI 模块".encode('utf-8')
print("Needle hex:", needle.hex())

# Check just the binary files
exts = {'.exe', '.dll', '.pyd', '.node', '.asar'}
hermes = r'D:\QClaw\v0.2.35.624'
count = 0
hits = []

for root, dirs, files in os.walk(hermes):
    for fn in files:
        _, ext = os.path.splitext(fn)
        if ext.lower() in exts or 'asar' in fn.lower():
            fp = os.path.join(root, fn)
            try:
                # Only read first 10MB of large files
                with open(fp, 'rb') as f:
                    data = f.read(10 * 1024 * 1024)
                if needle in data:
                    rel = fp.replace(hermes, '')
                    print(f'HIT: {rel} (read {len(data)} bytes)')
                    idx = data.index(needle)
                    print(f'  Context: {data[max(0,idx-50):idx+80]}')
                    hits.append(fp)
            except:
                pass
        count += 1

print(f'\nScanned {count} binary files, hits: {len(hits)}')

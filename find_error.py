import os, glob

# Search for the error string in binary across hermes libs
# "找不到 Hermes CLI 模块" in UTF-8
needle = "找不到 Hermes CLI 模块".encode('utf-8')
print(f"Searching for: {needle.hex()}")
print(f"Hex string: {'找不到 Hermes CLI 模块'.encode('utf-8').hex()}")

hermes = r'D:\QClaw\v0.2.35.624\resources\hermes'
count = 0
hits = []
for root, dirs, files in os.walk(hermes):
    for fn in files:
        fp = os.path.join(root, fn)
        try:
            with open(fp, 'rb') as f:
                data = f.read()
            idx = data.find(needle)
            if idx != -1:
                rel = fp.replace(hermes, '')
                print(f'\nFOUND in {rel}: {data[max(0,idx-50):idx+100]}')
                hits.append(fp)
        except:
            pass
        count += 1
        if count % 5000 == 0:
            print(f'Scanned {count}...')

print(f'\nTotal scanned: {count}, hits: {len(hits)}')

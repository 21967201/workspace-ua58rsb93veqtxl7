import os

needle = "找不到 Hermes CLI 模块"
hermes = r'D:\QClaw\v0.2.35.624\resources\hermes'
count = 0
hits = []

for root, dirs, files in os.walk(hermes):
    for fn in files:
        fp = os.path.join(root, fn)
        if fn.endswith(('.py', '.pyc', '.js', '.mjs')):
            try:
                with open(fp, 'rb') as f:
                    data = f.read()
                # Try UTF-8
                try:
                    txt = data.decode('utf-8')
                except:
                    try:
                        txt = data.decode('gbk')
                    except:
                        continue
                if needle in txt:
                    rel = fp.replace(hermes, '')
                    print(f'HIT: {rel}')
                    hits.append(fp)
            except:
                pass
        count += 1

print(f'Scanned {count} files, hits: {len(hits)}')

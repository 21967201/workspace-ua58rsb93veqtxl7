import os

needle = b'hermes-paths'
count = 0
hits = 0
root = r'D:\QClaw\v0.2.35.624\resources\hermes'
print('Starting search for:', repr(needle))
print('Root:', root)
for dirpath, dirs, files in os.walk(root):
    for fn in files:
        fp = os.path.join(dirpath, fn)
        try:
            with open(fp, 'rb') as f:
                data = f.read()
            if needle in data:
                idx = data.find(needle)
                print(f'HIT: {fp} at {idx} size:{len(data)}')
                hits += 1
            count += 1
        except Exception as e:
            pass
print(f'Done. searched={count} hits={hits}')

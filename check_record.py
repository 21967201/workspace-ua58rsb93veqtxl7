import os, csv, io

LIBS = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'
RECORD = os.path.join(LIBS, 'hermes_sdk-2026.6.19.dev12.dist-info', 'RECORD')

missing = []
total = 0
with open(RECORD, encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split(',')
        if len(parts) < 2:
            continue
        rel = parts[0]
        if rel.endswith('/') or '.dist-info/' in rel or rel.startswith('hermes_sdk-'):
            continue
        total += 1
        fp = os.path.join(LIBS, rel.replace('/', os.sep))
        if not os.path.exists(fp):
            missing.append(rel)

print(f'RECORD total files: {total}')
print(f'MISSING on disk: {len(missing)}')
if missing:
    print('\nFirst 40 missing:')
    for m in missing[:40]:
        print(' ', m)

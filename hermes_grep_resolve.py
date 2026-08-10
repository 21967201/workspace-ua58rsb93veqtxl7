import os, glob
libs = r'D:\QClaw\v0.2.35.624\resources\hermes\libs\hermes_cli'
patterns = ['def resolve_provider_client', 'def get_provider_client', 'def resolve_provider']
for f in glob.glob(os.path.join(libs, '**', '*.py'), recursive=True):
    try:
        with open(f, encoding='utf-8', errors='ignore') as fh:
            for i, line in enumerate(fh, 1):
                for p in patterns:
                    if p in line:
                        rel = f.replace(libs, '')
                        print(f'{rel}:{i}: {line.strip()}')
    except Exception:
        pass

import sys, os, inspect, glob
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')
os.environ['HERMES_HOME'] = r'C:\Users\Administrator\.hermes'

# 找 resolve_requested_provider（上游预处理 custom: 前缀）
import hermes_cli
src_files = glob.glob(r'D:\QClaw\v0.2.35.624\resources\hermes\libs\hermes_cli\**\*.py', recursive=True)

for fpath in src_files:
    try:
        with open(fpath, encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if 'resolve_requested_provider' in content or 'custom:' in content:
            # 找关键行
            for i, line in enumerate(content.splitlines(), 1):
                if ('resolve_requested_provider' in line or
                    ('custom:' in line and 'provider' in line.lower())):
                    print(f'{os.path.basename(fpath)}:{i}: {line.strip()}')
    except Exception:
        pass

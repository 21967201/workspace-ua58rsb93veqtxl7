import sys, os, json, pkgutil
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')
os.environ['HERMES_HOME'] = r'C:\Users\Administrator\.hermes'

# 找 provider 解析模块
import hermes_cli
print('hermes_cli submodules:', [m.name for m in pkgutil.iter_modules(hermes_cli.__path__)])
print('--- agent submodules ---')
import hermes_cli.agent as ag
print([m.name for m in pkgutil.iter_modules(ag.__path__)])

# 找 resolve_provider_client 真实位置
import subprocess
# 用 grep 在 libs 里找 resolve_provider_client 定义
import glob
hits = []
for f in glob.glob(r'D:\QClaw\v0.2.35.624\resources\hermes\libs\hermes_cli\**\*.py', recursive=True):
    try:
        with open(f, encoding='utf-8', errors='ignore') as fh:
            for i, line in enumerate(fh):
                if 'def resolve_provider_client' in line or 'def resolve_provider' in line or 'def get_provider_client' in line:
                    hits.append((f, i+1, line.strip()))
    except Exception:
        pass
print('=== resolve funcs found:', len(hits))
for h in hits[:10]:
    print(f'   {h[0].split("hermes_cli")[-1]}:{h[1]} {h[2]}')

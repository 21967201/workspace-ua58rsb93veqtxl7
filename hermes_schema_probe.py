import sys, os, re
os.environ['HERMES_HOME'] = r'C:\Users\Administrator\.hermes'
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')
from hermes_cli import config as cfg_mod
import inspect

src = inspect.getsource(cfg_mod)

# CONFIG_VERSION
for m in re.finditer(r'CONFIG_VERSION\s*=\s*(\d+)', src):
    print('CONFIG_VERSION =', m.group(1))

# find providers default structure - look for the default config dict
idx = src.find('"providers"')
if idx < 0:
    idx = src.find("'providers'")
if idx >= 0:
    print('--- providers context ---')
    print(src[max(0, idx-200):idx+2000])

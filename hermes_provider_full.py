import sys, os, inspect
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')
os.environ['HERMES_HOME'] = r'C:\Users\Administrator\.hermes'

from hermes_cli import auth
src = inspect.getsource(auth.resolve_provider)
# 打印完整源码，找 custom: 处理
print(src)

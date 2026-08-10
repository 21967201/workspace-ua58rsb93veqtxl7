import sys, os
# 模拟 QClaw launcher 进程：不预设 os.environ 里的 key（只继承注册表 HERMES_HOME）
# 真实场景：Electron spawn 时注入注册表 env → HERMES_HOME 已在环境
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')

# 先确认当前进程里的 HERMES_HOME
print('HERMES_HOME in env:', os.environ.get('HERMES_HOME'))

# 1. 验证 get_hermes_home 解析
from hermes_cli.config import get_hermes_home
hh = get_hermes_home()
print('get_hermes_home() =', hh)
from pathlib import Path; assert Path(hh).resolve() == Path(r'C:\Users\Administrator\.hermes').resolve(), f'WRONG HOME: {hh}'

# 2. 验证 load_hermes_dotenv 把 HERMES_ZHIPU_API_KEY 加载到 os.environ
from hermes_cli.env_loader import load_hermes_dotenv
loaded = load_hermes_dotenv(hermes_home=hh)
print('loaded env files:', loaded)
key = os.environ.get('HERMES_ZHIPU_API_KEY', '')
print('HERMES_ZHIPU_API_KEY in os.environ:', key[:14] + '...' if key else 'MISSING!')
assert key, 'HERMES_ZHIPU_API_KEY NOT loaded into os.environ!'

# 3. 用 runtime_provider 的 _getenv 解析（与模型调用同一路径）
from hermes_cli.runtime_provider import _getenv
k = _getenv('HERMES_ZHIPU_API_KEY', '')
print('runtime_provider._getenv(HERMES_ZHIPU_API_KEY) =', k[:14] + '...' if k else 'MISSING!')
assert k, '_getenv FAILED'

# 4. 用 _get_named_custom_provider 完整解析 custom:zhipu
from hermes_cli.runtime_provider import _get_named_custom_provider
entry = _get_named_custom_provider('custom:zhipu')
print('custom:zhipu entry:', entry)
assert entry and entry.get('api_key'), f'custom:zhipu resolution FAILED: {entry}'
assert entry.get('base_url') == 'https://open.bigmodel.cn/api/paas/v4', f'base_url wrong: {entry}'
print('FINAL: custom:zhipu -> base_url OK, api_key OK')

# 5. agnes 和 siliconflow 同理
for p in ['custom:agnes', 'custom:siliconflow']:
    e = _get_named_custom_provider(p)
    has_key = bool(e and e.get('api_key'))
    print(f'{p}: resolved={"OK" if has_key else "FAIL"} key={e.get("api_key","")[:10] if e else None}... base_url={e.get("base_url") if e else None}')

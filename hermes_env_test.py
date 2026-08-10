import sys, os
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')
os.environ['HERMES_HOME'] = r'C:\Users\Administrator\.hermes'

from hermes_cli.config import get_env_value_prefer_dotenv, load_config
from hermes_cli import auth

cfg = load_config()

# 1. 验证 get_env_value_prefer_dotenv 能读到 HERMES_ZHIPU_API_KEY
for var in ['HERMES_ZHIPU_API_KEY', 'ZHIPU_API_KEY']:
    val = get_env_value_prefer_dotenv(var)
    print(f'get_env_value_prefer_dotenv({var}) = {val[:12] if val else None}...')

# 2. 看 custom provider 的解析：custom:zhipu 如何走
print()
print('=== model.provider:', cfg['model']['provider'])
model_cfg = cfg.get('model', {})
print('model_cfg keys:', list(model_cfg.keys()))

# 3. 尝试直接调用 auth.resolve_provider 看 custom:zhipu 的解析结果
import inspect
try:
    src = inspect.getsource(auth.resolve_provider)
    print('=== auth.resolve_provider source (first 2500 chars) ===')
    print(src[:2500])
except Exception as e:
    print('resolve_provider src err:', e)

import sys, os, json
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')
os.environ['HERMES_HOME'] = r'C:\Users\Administrator\.hermes'

# 用 hermes 内部 API 解析模型 provider，验证 custom:zhipu 是否能正确解析
from hermes_cli.config import load_config
cfg = load_config()

# 1. 检查 hermes 是否把 custom:zhipu 映射到 providers.zhipu
print('=== model.provider:', cfg['model']['provider'])
print('=== providers keys:', list(cfg.get('providers', {}).keys()))
print('=== models list:')
for m in cfg.get('models', []):
    print(f"   {m['name']} -> {m.get('provider')} (prio {m.get('priority')})")
print('=== model_aliases:', json.dumps(cfg.get('model_aliases', {}), ensure_ascii=False))

# 2. 探测 hermes 内部 provider 解析函数
import hermes_cli.llm as llm_mod
import inspect
# 找 provider/client 解析函数
cands = [n for n in dir(llm_mod) if 'provider' in n.lower() or 'client' in n.lower() or 'resolve' in n.lower()]
print('=== llm module resolve funcs:', cands)

# 尝试用 llm 模块解析 custom provider
try:
    from hermes_cli.llm import get_llm_client, resolve_provider
    # 看看 signature
    for f in [get_llm_client, resolve_provider]:
        try:
            print(f'   {f.__name__}{inspect.signature(f)}')
        except Exception as e:
            print(f'   {f.__name__}: sig err {e}')
except ImportError as e:
    print('llm import err:', e)

# 3. 检查 auxiliary 使用的 key 解析
try:
    from hermes_cli.agent.auxiliary_client import resolve_provider_client
    print('auxiliary resolve_provider_client found:', resolve_provider_client)
except ImportError as e:
    print('auxiliary import err:', e)
    # 尝试其它路径
    import pkgutil
    import hermes_cli.agent as ag
    print('agent submodules:', [m.name for m in pkgutil.iter_modules(ag.__path__)])

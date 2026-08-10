import sys, os, json
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')
os.environ['HERMES_HOME'] = r'C:\Users\Administrator\.hermes'

results = []

def check(name, fn):
    try:
        fn()
        results.append(('PASS', name))
    except Exception as e:
        results.append(('FAIL', f'{name}: {e}'))

# 1. config.yaml 加载（无警告）
def t_config():
    from hermes_cli.config import load_config
    cfg = load_config()
    assert cfg.get('_config_version') == 33, f"version={cfg.get('_config_version')}"
    assert cfg['model']['default'] == 'glm-4-flash'
    assert cfg['model']['provider'] == 'custom:zhipu'
    prov = cfg.get('providers', {})
    assert 'zhipu' in prov and 'agnes' in prov and 'siliconflow' in prov
    # 无旧字段
    for k, v in prov.items():
        assert 'type' not in v, f'{k} has legacy type'
        assert 'max_tokens' not in v, f'{k} has legacy max_tokens'
    print('   providers:', list(prov.keys()))
    print('   default model:', cfg['model']['default'], cfg['model']['provider'])
check('config.yaml v33 加载', t_config)

# 2. .env 加载 + key 解析
def t_env():
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.environ['HERMES_HOME'], '.env'), override=True)
    from hermes_cli.config import load_config
    cfg = load_config()
    # 模拟 hermes_cli 的 key 解析：key_env 优先，其次 api_key 明文
    for name, p in cfg.get('providers', {}).items():
        if 'key_env' in p:
            key = os.environ.get(p['key_env'])
            assert key and key != '', f'{name} key_env={p["key_env"]} unset'
            print(f'   {name}: key via env {p["key_env"]} = {key[:12]}...')
        elif 'api_key' in p:
            assert p['api_key'], f'{name} empty api_key'
            print(f'   {name}: inline key {p["api_key"][:12]}...')
check('.env key 解析', t_env)

# 3. 三个 provider 真实调用
def t_zhipu():
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.environ['HERMES_HOME'], '.env'), override=True)
    c = OpenAI(api_key=os.environ['HERMES_ZHIPU_API_KEY'], base_url='https://open.bigmodel.cn/api/paas/v4')
    r = c.chat.completions.create(model='glm-4-flash', messages=[{'role':'user','content':'ping'}], max_tokens=5)
    print('   glm-4-flash OK:', r.choices[0].message.content[:30])
check('zhipu glm-4-flash 调用', t_zhipu)

def t_agnes():
    from openai import OpenAI
    c = OpenAI(api_key='sk-ajjCwdZzu7w3xMybVhJ5DjjwozeeZNY7tU2kIFWvrvReFvQF', base_url='https://apihub.agnes-ai.cn/v1')
    r = c.chat.completions.create(model='agnes-2.0-flash', messages=[{'role':'user','content':'ping'}], max_tokens=5)
    print('   agnes-2.0-flash OK:', r.choices[0].message.content[:30])
check('agnes agnes-2.0-flash 调用', t_agnes)

def t_silicon():
    from openai import OpenAI
    c = OpenAI(api_key='sk-jqmtkodepqlsokgnjrxhjvvyrmubchbzdsncuwznpffhbgfq', base_url='https://api.siliconflow.cn/v1')
    r = c.chat.completions.create(model='Qwen/Qwen3-8B', messages=[{'role':'user','content':'ping'}], max_tokens=5)
    print('   Qwen3-8B OK:', r.choices[0].message.content[:30])
check('siliconflow Qwen3-8B 调用', t_silicon)

# 4. MCP servers 配置
def t_mcp():
    from hermes_cli.config import load_config
    cfg = load_config()
    servers = cfg.get('mcp_servers', {})
    assert 'time' in servers and 'everything' in servers and 'filesystem' in servers
    print('   mcp_servers:', list(servers.keys()))
check('MCP servers 配置', t_mcp)

# 5. API server 配置
def t_api():
    from hermes_cli.config import load_config
    cfg = load_config()
    ap = cfg.get('platforms', {}).get('api_server', {})
    assert ap.get('enabled') is True
    print('   api_server port:', ap.get('extra', {}).get('port'))
check('API server 配置', t_api)

for status, name in results:
    print(f'[{status}] {name}')

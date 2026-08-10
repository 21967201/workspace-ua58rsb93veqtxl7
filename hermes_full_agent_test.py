import sys, os
# 完全模拟 QClaw launcher 环境：libs 为 PYTHONPATH
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')
os.environ['HERMES_HOME'] = r'C:\Users\Administrator\.hermes'
os.environ.pop('PYTHONPATH', None)

# 走 run_agent 的真实入口：模拟 -z 单次对话（agent 主循环 + 模型调用）
# 先验证 run_agent 能加载且 .env 被正确加载
from hermes_cli.env_loader import load_hermes_dotenv
from hermes_cli.config import get_hermes_home

hh = get_hermes_home()
loaded = load_hermes_dotenv(hermes_home=hh)
print('env loaded:', loaded)
print('key present:', bool(os.environ.get('HERMES_ZHIPU_API_KEY')))

# 直接走 auxiliary_client.resolve_provider_client（旧日志报错处）
from agent.auxiliary_client import resolve_provider_client
client, model = resolve_provider_client('custom:zhipu', model='glm-4-flash')
print('client resolved:', type(client).__name__, '| model:', model)
assert client is not None, 'client resolution FAILED'

# 真实调用
resp = client.chat.completions.create(
    model='glm-4-flash',
    messages=[{'role': 'user', 'content': '回复两个字：正常'}],
    max_tokens=20
)
print('AGENT TURN OK:', resp.choices[0].message.content)
print('usage:', resp.usage)
print('=== FULL CHAIN PASS ===')

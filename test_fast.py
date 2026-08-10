import sys, os

LIBS = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'
sys.path.insert(0, LIBS)

print('=== Quick import tests ===')

tests = [
    ('hermes_cli.__main__', lambda: __import__('hermes_cli.__main__')),
    ('hermes_cli.main', lambda: __import__('hermes_cli.main')),
    ('hermes_cli_main_', lambda: __import__('hermes_cli_main_')),
    ('gateway.platforms.telegram', lambda: __import__('gateway.platforms.telegram')),
    ('gateway.platforms.slack', lambda: __import__('gateway.platforms.slack')),
    ('gateway.platforms.feishu', lambda: __import__('gateway.platforms.feishu')),
    ('gateway.platforms.whatsapp', lambda: __import__('gateway.platforms.whatsapp')),
    ('gateway.platforms.wecom', lambda: __import__('gateway.platforms.wecom')),
    ('gateway.platforms.dingtalk', lambda: __import__('gateway.platforms.dingtalk')),
    ('gateway.platforms.matrix', lambda: __import__('gateway.platforms.matrix')),
    ('plugins.cron', lambda: __import__('plugins.cron')),
    ('plugins.cron.chronos', lambda: __import__('plugins.cron.chronos')),
    ('tools.mixture_of_agents_tool', lambda: __import__('tools.mixture_of_agents_tool')),
    ('agent.gemini_cloudcode_adapter', lambda: __import__('agent.gemini_cloudcode_adapter')),
    ('agent.google_code_assist', lambda: __import__('agent.google_code_assist')),
]

for name, fn in tests:
    try:
        fn()
        print(f'  [OK]  {name}')
    except Exception as e:
        print(f'  [FAIL] {name}: {type(e).__name__}: {str(e)[:100]}')

print('\nAll tests done.')

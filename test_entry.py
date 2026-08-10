import sys, os

LIBS = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'
sys.path.insert(0, LIBS)

print('=== Test 1: python -m hermes_cli (main entry) ===')
try:
    import hermes_cli.__main__ as m
    print('hermes_cli.__main__ loaded OK')
    print('  has main:', hasattr(m, 'main') or callable(getattr(m, 'main', None)))
except Exception as e:
    print(f'  FAIL: {type(e).__name__}: {e}')

print('\n=== Test 2: hermes_cli.main.main callable ===')
try:
    import hermes_cli.main as main_mod
    print('  main callable:', callable(main_mod.main))
except Exception as e:
    print(f'  FAIL: {type(e).__name__}: {e}')

print('\n=== Test 3: compat entry hermes_cli_main_.py ===')
try:
    import hermes_cli_main_
    print('  loaded OK, main callable:', callable(hermes_cli_main_.main))
except Exception as e:
    print(f'  FAIL: {type(e).__name__}: {e}')

print('\n=== Test 4: gateway.platforms modules import ===')
for mod in ['gateway.platforms.telegram', 'gateway.platforms.slack', 'gateway.platforms.feishu', 'gateway.platforms.whatsapp', 'gateway.platforms.wecom']:
    try:
        __import__(mod)
        print(f'  {mod}: OK')
    except Exception as e:
        print(f'  {mod}: FAIL {type(e).__name__}: {str(e)[:80]}')

print('\n=== Test 5: plugins.cron modules ===')
for mod in ['plugins.cron', 'plugins.cron.chronos']:
    try:
        __import__(mod)
        print(f'  {mod}: OK')
    except Exception as e:
        print(f'  {mod}: FAIL {type(e).__name__}: {str(e)[:80]}')

print('\n=== Test 6: tools.mixture_of_agents_tool ===')
try:
    __import__('tools.mixture_of_agents_tool')
    print('  tools.mixture_of_agents_tool: OK')
except Exception as e:
    print(f'  FAIL: {type(e).__name__}: {str(e)[:80]}')

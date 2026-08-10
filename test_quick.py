import sys, os, faulthandler, time
faulthandler.enable()

sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')

tests = [
    'hermes_cli',
    'hermes_cli.main',
    'hermes_cli.__main__',
    'hermes_cli_main_',
    'gateway.platforms.telegram',
    'gateway.platforms.slack',
    'gateway.platforms.feishu',
    'plugins.cron',
    'plugins.cron.chronos',
    'agent.gemini_cloudcode_adapter',
]

for name in tests:
    t0 = time.time()
    try:
        __import__(name)
        dt = (time.time() - t0) * 1000
        print(f'[OK]  {name} ({dt:.0f}ms)', flush=True)
    except Exception as e:
        dt = (time.time() - t0) * 1000
        print(f'[FAIL] {name} ({dt:.0f}ms): {type(e).__name__}: {str(e)[:80]}', flush=True)

import sys, os, importlib

LIBS = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'
sys.path.insert(0, LIBS)

results = []

def check(name, fn):
    try:
        r = fn()
        results.append((name, 'OK', str(r)[:100]))
    except Exception as e:
        results.append((name, 'FAIL', f'{type(e).__name__}: {e}'))

# 1. Compat entry file exists on disk
check('compat file exists', lambda: os.path.exists(os.path.join(LIBS, 'hermes_cli_main_.py')))

# 2. Compat entry imports cleanly
def _import_compat():
    import hermes_cli_main_
    return callable(hermes_cli_main_.main)
check('import hermes_cli_main_', _import_compat)

# 3. Real main module loads
def _import_main():
    import hermes_cli.main
    return callable(hermes_cli.main.main)
check('import hermes_cli.main', _import_main)

# 4. hermes-paths module existence
def _hp():
    try:
        importlib.import_module('hermes-paths')
        return 'module exists'
    except ModuleNotFoundError:
        return 'module NOT found (logger-name only)'
check('hermes-paths module', _hp)

# 5. hermes_sdk package dir
check('hermes_sdk dir', lambda: os.path.isdir(os.path.join(LIBS, 'hermes_sdk')))

# 6. libs/bin/hermes.exe shim exists
check('hermes.exe shim', lambda: os.path.exists(os.path.join(LIBS, 'bin', 'hermes.exe')))

for name, status, detail in results:
    print(f'[{status}] {name}: {detail}')

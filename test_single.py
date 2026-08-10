import sys, os, faulthandler
faulthandler.enable()

LIBS = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'
sys.path.insert(0, LIBS)

print('starting import test...', flush=True)
try:
    import hermes_cli
    print('hermes_cli package import OK', flush=True)
    print('modules:', [x for x in dir(hermes_cli) if not x.startswith('_')][:20], flush=True)
except Exception as e:
    print(f'FAIL: {type(e).__name__}: {e}', flush=True)

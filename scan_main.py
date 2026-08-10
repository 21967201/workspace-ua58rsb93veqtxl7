import os

# Try to find files that CONSTRUCT the path, not contain it
# Search for patterns like "hermes_cli" + "main" together
hermes = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'

hits = []
for root, dirs, files in os.walk(hermes):
    for fn in files:
        if fn.endswith('.py'):
            fp = os.path.join(root, fn)
            try:
                with open(fp, 'rb') as f:
                    data = f.read()
                try:
                    txt = data.decode('utf-8')
                except:
                    txt = data.decode('gbk', errors='replace')
                # Look for logger named 'hermes-paths' or logging.getLogger('hermes-paths')
                if "getLogger('hermes-paths')" in txt or 'getLogger("hermes-paths")' in txt or "logger = getLogger('hermes-paths')" in txt:
                    print('LOGGER HIT:', fp)
                    hits.append(fp)
            except:
                pass

print('Logger hits:', len(hits))

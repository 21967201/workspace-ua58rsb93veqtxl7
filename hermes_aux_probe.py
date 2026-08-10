import sys
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')
with open(r'D:\QClaw\v0.2.35.624\resources\hermes\libs\agent\auxiliary_client.py', encoding='utf-8', errors='ignore') as f:
    content = f.read()
idx = content.find('def resolve_provider_client')
seg = content[idx:idx+20000]
for key in ['key_env', 'custom_providers', "config.get('providers'", 'load_config', 'providers.get', "cfg['providers']", 'named custom']:
    i = seg.find(key)
    if i >= 0:
        print(f'--- found "{key}" at offset {i} ---')
        print(seg[max(0,i-250):i+500])
        print()

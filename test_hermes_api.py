"""测试 qclaw_launcher / 8642 端口的实际 Hermes API"""
import json, sys, urllib.request, urllib.error

# 从 config.yaml 读 API key
import yaml
config_path = r'C:\Users\Administrator\.qclaw-hermes\config.yaml'
with open(config_path, encoding='utf-8') as f:
    config = yaml.safe_load(f)

# API key 从 auth gateway 管理，可能是固定值或从 credential 获取
# 先试试不带 auth 或用简单 token
base_url = 'http://127.0.0.1:8642'

paths_to_test = [
    '/api/health',
    '/api/status',
    '/healthz',
    '/api/v1/status',
    '/api/agent/status',
    '/api/sessions',
    '/',
]

for path in paths_to_test:
    try:
        req = urllib.request.Request(base_url + path)
        req.add_header('Content-Type', 'application/json')
        try:
            resp = urllib.request.urlopen(req, timeout=3)
            print(f'{path}: {resp.status} {resp.read(200).decode()[:100]}')
        except urllib.error.HTTPError as e:
            print(f'{path}: HTTP {e.code} {e.read(200).decode()[:100] if e.fp else ""}')
        except Exception as e:
            print(f'{path}: ERR {type(e).__name__}: {e}')
    except Exception as e:
        print(f'{path}: REQ ERR {e}')

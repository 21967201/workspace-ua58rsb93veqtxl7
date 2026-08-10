import os, sys, struct

base = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'

# Search for 'hermes-paths' in ALL files (including pyc, pyd) under hermes libs
# but limit to smaller dirs (skip huge site-packages-like dirs)
needle = b'hermes-paths'
needle2 = b'hermes_cli_main_'
needle3 = '找不到 Hermes CLI 模块'.encode('utf-8')

count = 0
hits = []

SKIP_DIRS = {'google_api', 'botocore', 'boto3', 'aiohttp', 'cryptography', 'opentelemetry',
             'msal', 'azure', 'alibabacloud', 'dingtalk', 'daytona', 'lark_oapi', 'modal',
             'python_telegram', 'slack', 'discord', 'tencent', 'urllib3', 'requests',
             'pydantic', 'anthropic', 'openai', 'websockets', 'uvicorn', 'starlette',
             'win32', 'pythonwin', 'PIL', 'google', 'Crypto', 'protobuf', 'grpclib',
             'ruamel', 'yaml', 'jinja2', 'rich', 'prompt_toolkit', 'click', 'fire',
             'apscheduler', 'croniter', 'httpx', 'httpcore', 'h2', 'hpack', 'hyperframe',
             'frozenlist', 'multidict', 'propcache', 'yarl', 'aiosignal', 'attrs',
             'pydantic_core', 'rpds', 'referencing', 'jsonschema', 'markdown', 'toml',
             'tqdm', 'tenacity', 'watchfiles', 'tzlocal', 'tzdata', 'portalocker',
             'packaging', 'psutil', 'bcrypt', 'cffi', 'pycparser', 'charset_normalizer',
             'idna', 'certifi', 'importlib_metadata', 'zipp', 'typing_extensions',
             'six', 'dateutil', 'oauthlib', 'requests_oauthlib', 'socksio', 'sniffio',
             'anyio', 'exceptiongroup', 'h11', 'sse_starlette', 'multipart', 'python_multipart',
             'environs', 'marshmallow', 'python_dotenv', 'dotenv', 'distro', 'pathspec',
             's3transfer', 'jmespath', 'pyasn1', 'pyasn1_modules', 'rfc3986', 'deprecated',
             'wrapt', 'tabulate', 'wcwidth', 'shellingham', 'typer', 'colorama',
             'pygments', 'simple_term_menu', 'edge_tts', 'elevenlabs', 'firecrawl',
             'exa_py', 'fal_client', 'googleapiclient', 'httplib2', 'uritemplate',
             'honcho', 'hindsight_client', 'obstore', 'nemo_relay', 'parallel',
             'modal', 'daytona', 'qrcode', 'synchronicity', 'acp', 'acp_adapter',
             'tools', 'providers', 'optional-mcps', 'optional-skills'}

def should_skip(path):
    parts = set(path.replace('\\', '/').split('/'))
    return bool(parts & SKIP_DIRS)

for root, dirs, files in os.walk(base):
    if should_skip(root):
        continue
    for fn in files:
        fp = os.path.join(root, fn)
        try:
            with open(fp, 'rb') as f:
                data = f.read(2 * 1024 * 1024)
            for needle, label in [(needle, 'hermes-paths'), (needle2, 'hermes_cli_main_'), (needle3, 'err-msg')]:
                if needle in data:
                    rel = fp.replace(base, '')
                    idx = data.index(needle)
                    ctx = data[max(0, idx-40):idx+60]
                    print(f'HIT [{label}] {rel}:')
                    print(f'  ctx: {ctx!r}')
                    hits.append((fp, label))
                    break
        except Exception:
            pass
        count += 1
        if count % 2000 == 0:
            print(f'  ...scanned {count}', flush=True)

print(f'\nTotal scanned: {count}, hits: {len(hits)}')

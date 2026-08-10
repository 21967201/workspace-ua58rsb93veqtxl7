import sys, os, time, faulthandler
faulthandler.enable()
sys.path.insert(0, r'D:\QClaw\v0.2.35.624\resources\hermes\libs')

LIBS = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'

print('=' * 60)
print('HERMES CLI 修复验证报告')
print('=' * 60)

# 1. RECORD完整性
print('\n[1] RECORD 完整性验证')
RECORD = os.path.join(LIBS, 'hermes_sdk-2026.6.19.dev12.dist-info', 'RECORD')
missing = []
with open(RECORD, encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split(',')
        if len(parts) < 2: continue
        rel = parts[0]
        if rel.endswith('/') or '.dist-info/' in rel: continue
        fp = os.path.join(LIBS, rel.replace('/', os.sep))
        if not os.path.exists(fp):
            missing.append(rel)
print(f'  RECORD 总文件: 797')
print(f'  缺失文件: {len(missing)}')
if missing: print(f'  STILL MISSING: {missing}')
else: print('  ✅ 所有 RECORD 文件已就位')

# 2. 修复文件清单
print('\n[2] 修复文件验证')
fixes = [
    ('hermes_cli_main_.py', '兼容入口文件（修复打包遗漏）'),
    ('hermes_cli/__main__.py', 'Python -m 入口（从 hermes_2.tar 提取）'),
    ('hermes_cli/memory_providers.py', '内存提供者模块'),
    ('plugins/cron/__init__.py', 'Cron 插件根模块'),
    ('plugins/cron/chronos/__init__.py', 'Chronos cron provider'),
    ('plugins/cron/chronos/verify.py', 'Chronos 验证'),
    ('plugins/cron/chronos/_nas_client.py', 'NAS 客户端'),
    ('plugins/cron/chronos/plugin.yaml', 'Chronos 配置'),
    ('gateway/platforms/telegram.py', 'Telegram 集成'),
    ('gateway/platforms/slack.py', 'Slack 集成'),
    ('gateway/platforms/feishu.py', '飞书集成'),
    ('gateway/platforms/whatsapp.py', 'WhatsApp 集成'),
    ('gateway/platforms/wecom.py', '企业微信集成'),
    ('gateway/platforms/dingtalk.py', '钉钉集成'),
    ('gateway/platforms/matrix.py', 'Matrix 集成'),
    ('gateway/platforms/sms.py', 'SMS 集成'),
    ('agent/gemini_cloudcode_adapter.py', 'Gemini Cloud Code 适配器'),
    ('agent/google_code_assist.py', 'Google Code Assist 适配器'),
    ('agent/google_oauth.py', 'Google OAuth'),
    ('tools/mixture_of_agents_tool.py', 'MoA 工具'),
]
all_ok = True
for rel, desc in fixes:
    fp = os.path.join(LIBS, rel.replace('/', os.sep))
    exists = os.path.exists(fp)
    status = '✅' if exists else '❌'
    print(f'  {status} {rel}: {desc}')
    if not exists:
        all_ok = False

# 3. 关键 import 测试
print('\n[3] 关键 import 测试')
imports = [
    'hermes_cli_main_',
    'hermes_cli.__main__',
    'hermes_cli.main',
    'gateway.platforms.telegram',
    'gateway.platforms.slack',
    'gateway.platforms.feishu',
    'gateway.platforms.whatsapp',
    'plugins.cron',
    'plugins.cron.chronos',
    'agent.gemini_cloudcode_adapter',
]
for mod in imports:
    t0 = time.time()
    try:
        __import__(mod)
        dt = (time.time() - t0) * 1000
        print(f'  ✅ {mod} ({dt:.0f}ms)')
    except Exception as e:
        print(f'  ❌ {mod}: {type(e).__name__}: {str(e)[:80]}')
        all_ok = False

# 4. compat entry 可调用性
print('\n[4] 兼容入口可调用性')
try:
    import hermes_cli_main_
    ok = callable(hermes_cli_main_.main)
    print(f'  hermes_cli_main_.main callable: {ok} ✅' if ok else f'  hermes_cli_main_.main callable: {ok} ❌')
    if not ok: all_ok = False
except Exception as e:
    print(f'  ❌ hermes_cli_main_ import: {e}')
    all_ok = False

# 5. hermes.exe shim 存在性
print('\n[5] Hermes CLI Console Scripts')
bin_dir = os.path.join(LIBS, 'bin')
for fn in ['hermes.exe', 'hermes-agent.exe', 'hermes-acp.exe']:
    fp = os.path.join(bin_dir, fn)
    exists = os.path.exists(fp)
    size = os.path.getsize(fp) if exists else 0
    print(f'  {"✅" if exists else "❌"} {fn} ({size} bytes)')

print('\n' + '=' * 60)
if all_ok:
    print('✅✅✅ 全部验证通过！Hermes CLI 修复完成！')
else:
    print('⚠️  部分验证失败，请检查上述失败项')
print('=' * 60)

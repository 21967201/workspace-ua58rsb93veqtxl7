import os, tarfile, io

LIBS = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'
TAR = r'D:\QClaw\v0.2.35.624\resources\hermes_2.tar'

MISSING = [
    'agent/gemini_cloudcode_adapter.py',
    'agent/google_code_assist.py',
    'agent/google_oauth.py',
    'gateway/platforms/dingtalk.py',
    'gateway/platforms/email.py',
    'gateway/platforms/feishu.py',
    'gateway/platforms/feishu_comment.py',
    'gateway/platforms/feishu_comment_rules.py',
    'gateway/platforms/feishu_meeting_invite.py',
    'gateway/platforms/matrix.py',
    'gateway/platforms/slack.py',
    'gateway/platforms/sms.py',
    'gateway/platforms/telegram.py',
    'gateway/platforms/telegram_network.py',
    'gateway/platforms/wecom.py',
    'gateway/platforms/wecom_callback.py',
    'gateway/platforms/wecom_crypto.py',
    'gateway/platforms/whatsapp.py',
    'hermes_cli/__main__.py',
    'hermes_cli/memory_providers.py',
    'plugins/cron/__init__.py',
    'plugins/cron/chronos/__init__.py',
    'plugins/cron/chronos/_nas_client.py',
    'plugins/cron/chronos/plugin.yaml',
    'plugins/cron/chronos/verify.py',
    'tools/mixture_of_agents_tool.py',
]

tf = tarfile.open(TAR, 'r')
extracted = 0
not_found = []
for rel_path in MISSING:
    # hermes_sdk entries in tar are under 'hermes_sdk/' prefix
    members = [m for m in tf.getmembers() if m.name.endswith(rel_path)]
    if not members:
        # try without hermes_sdk prefix
        members = [m for m in tf.getmembers() if m.name == rel_path or m.name == 'hermes_sdk/' + rel_path]
    
    for m in members:
        # Extract
        dest = os.path.join(LIBS, rel_path.replace('/', os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with tf.extractfile(m) as src:
            data = src.read()
        with open(dest, 'wb') as dst:
            dst.write(data)
        extracted += 1
        print(f'  Extracted: {rel_path} ({len(data)} bytes)')
        break
    else:
        not_found.append(rel_path)

tf.close()

print(f'\nExtracted: {extracted}/{len(MISSING)}')
if not_found:
    print(f'NOT FOUND in tar: {not_found}')
else:
    print('All files extracted successfully.')

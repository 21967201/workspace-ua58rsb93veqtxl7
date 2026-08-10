import os, tarfile

LIBS = r'D:\QClaw\v0.2.35.624\resources\hermes\libs'
TARS = [
    r'D:\QClaw\v0.2.35.624\resources\hermes_0.tar',
    r'D:\QClaw\v0.2.35.624\resources\hermes_1.tar',
    r'D:\QClaw\v0.2.35.624\resources\hermes_2.tar',
]

MISSING = [
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
    'tools/mixture_of_agents_tool.py',
]

# Build a name->member map for all tars
name_map = {}
for tar_path in TARS:
    tf = tarfile.open(tar_path, 'r')
    for m in tf.getmembers():
        if m.isfile():
            name_map[m.name] = (tar_path, m)
    tf.close()

extracted = 0
not_found = []
for rel in MISSING:
    candidates = []
    # Try various prefixes
    for prefix in ['', 'hermes_sdk/', 'hermes/', 'libs/', 'hermes/libs/']:
        key = prefix + rel
        if key in name_map:
            candidates.append(key)
    if not candidates:
        # fuzzy: any member ending with the rel path
        fuzzy = [k for k in name_map if k.endswith(rel)]
        candidates = fuzzy
    if candidates:
        # Prefer exact prefix match, else longest suffix
        key = candidates[0] if candidates else None
        if len(candidates) > 1:
            # prefer shortest key (most exact)
            key = sorted(candidates, key=len)[0]
        tar_path, member = name_map[key]
        tf = tarfile.open(tar_path, 'r')
        dest = os.path.join(LIBS, rel.replace('/', os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with tf.extractfile(member) as src:
            data = src.read()
        with open(dest, 'wb') as dst:
            dst.write(data)
        tf.close()
        extracted += 1
        print(f'  Extracted {rel} <- {key} ({len(data)}B)')
    else:
        not_found.append(rel)

print(f'\nExtracted: {extracted}/{len(MISSING)}')
if not_found:
    print(f'NOT FOUND anywhere: {not_found}')
else:
    print('All remaining files extracted.')

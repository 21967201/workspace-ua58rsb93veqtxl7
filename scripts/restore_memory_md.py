import subprocess, io
ref = '08c5d5a'
data = subprocess.check_output(['git','show',f'{ref}:MEMORY.md'], stderr=subprocess.STDOUT)
# 08c5d5a blob is GBK-encoded and clean (gbk_FFFD=0)
text = data.decode('gbk')
fffd = text.count('\ufffd')
print("decoded gbk, FFFD count:", fffd)
# Re-encode as UTF-8 with BOM
out = '﻿' + text
with io.open('MEMORY.md','w',encoding='utf-8') as f:
    f.write(out)
# Verify
raw = open('MEMORY.md','rb').read()
print("written bytes:", len(raw), "BOM:", raw[:3].hex())
rt = raw.decode('utf-8')
print("utf8 re-decode FFFD:", rt.count('\ufffd'))
print("contains 07-21 record:", '2026-07-21' in rt)
print("contains 07-20 consolidation report:", 'Memory Consolidation Report (2026-07-20)' in rt)

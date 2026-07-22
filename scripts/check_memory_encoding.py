import subprocess
refs = ['08c5d5a','dc1d19f','c3131fb','db904a1a','f3fb8d9']
for ref in refs:
    try:
        data = subprocess.check_output(['git','show',f'{ref}:MEMORY.md'], stderr=subprocess.DEVNULL)
    except Exception as e:
        print(ref, 'ERR', e); continue
    utf8_fffd = -1; gbk_ok=False; gbk_fffd=-1
    try:
        t = data.decode('utf-8')
        utf8_fffd = t.count('\ufffd')
    except Exception:
        pass
    try:
        t2 = data.decode('gbk')
        gbk_ok = True
        gbk_fffd = t2.count('\ufffd')
    except Exception:
        gbk_ok=False
    print(f"{ref}: bytes={len(data)} utf8_FFFD={utf8_fffd} gbk_decodable={gbk_ok} gbk_FFFD={gbk_fffd}")

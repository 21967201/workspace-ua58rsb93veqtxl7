# -*- coding: utf-8 -*-
import os, json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\Administrator\.qclaw\workspace\sessions"
import datetime
CUTOFF = datetime.datetime.now() - datetime.timedelta(days=30)

def read_gbk(path):
    raw = open(path, 'rb').read()
    try:
        return raw.decode('utf-8')
    except Exception:
        return raw.decode('gbk', errors='replace')

targets = ["记忆整理", "记忆提升", "会话摘要", "Distill发现", "技术监控"]
for d in os.listdir(BASE):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    # recent?
    recent = False
    for root,_,files in os.walk(dp):
        for fn in files:
            try:
                if datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root,fn)))>=CUTOFF:
                    recent=True;break
            except:pass
        if recent:break
    if not recent:continue
    name=""
    sp=os.path.join(dp,"store.json")
    if os.path.exists(sp):
        try: name=json.loads(read_gbk(sp)).get("name","")
        except:pass
    if name in targets:
        print("="*60)
        print("NAME:",name,"  DIR:",d)
        print("="*60)
        for fn in sorted(os.listdir(dp)):
            if fn.startswith("summary_") and fn.endswith(".md"):
                txt=read_gbk(os.path.join(dp,fn))
                print(txt.strip()[:1500])
                print()

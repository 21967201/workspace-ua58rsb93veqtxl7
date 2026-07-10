# -*- coding: utf-8 -*-
import os, json
BASE = r"C:\Users\Administrator\.qclaw\workspace\sessions"
for d in sorted(os.listdir(BASE)):
    dp = os.path.join(BASE, d)
    if not os.path.isdir(dp):
        continue
    sp = os.path.join(dp, "store.json")
    if not os.path.exists(sp):
        continue
    raw = open(sp, "rb").read()
    # try utf-8 first
    try:
        name = json.loads(raw.decode("utf-8")).get("name", "")
        enc = "utf-8"
    except Exception:
        try:
            name = json.loads(raw.decode("gbk")).get("name", "")
            enc = "gbk"
        except Exception:
            name = repr(raw[:60]); enc = "?"
    print("%s  [%s]  %r" % (d[:12], enc, name))

# -*- coding: utf-8 -*-
import os, json
from pypdf import PdfReader
BASE=r"d:/READING/Books"
new=[f for f in os.listdir(BASE) if f.lower().endswith('.pdf')]
out=[]
for f in sorted(new):
    p=os.path.join(BASE,f)
    rec={"file":f,"npages":0,"title":"","text":""}
    try:
        r=PdfReader(p); rec["npages"]=len(r.pages)
        md=r.metadata or {}; rec["title"]=(md.get("/Title") or "").strip()
        t=""
        for i in range(min(4,len(r.pages))):
            try:t+=(r.pages[i].extract_text() or "")+" "
            except:pass
            if len(t)>700:break
        rec["text"]=" ".join(t.split())[:700]
    except Exception as e:
        rec["err"]=str(e)[:100]
    out.append(rec)
open(r"d:/READING/_library_build/new_probe.json","w",encoding="utf-8").write(json.dumps(out,ensure_ascii=False,indent=1))
print("done",len(out))

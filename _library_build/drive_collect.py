# -*- coding: utf-8 -*-
"""Scrape a public Google Drive folder tree and map filename -> file id."""
import re, json, subprocess, sys, time, os

ROOT = "1kIpTbRnVZQIO8AFEYrJ9ySVf8qcGhFAc"
HDR = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

ENTRY = re.compile(r'\["([A-Za-z0-9_-]{20,})",\["([A-Za-z0-9_-]{20,})"\],"((?:[^"\\]|\\.)*?)","(application/[^"]+)"')

def fetch(fid):
    url = "https://drive.google.com/drive/folders/%s" % fid
    out = subprocess.run(["curl","-sL","-A",HDR,url], capture_output=True)
    return out.stdout.decode("utf-8","replace")

def ivd(html):
    m = re.search(r"_DRIVE_ivd'\] = '(.*?)';", html, re.S)
    if not m: return ""
    s = m.group(1)
    s = re.sub(r"\\x([0-9a-fA-F]{2})", lambda x: chr(int(x.group(1),16)), s)
    s = s.replace("\\/", "/")
    return s

def deesc(s):
    out=[]; i=0
    while i < len(s):
        if s[i]=="\\" and i+1<len(s):
            c=s[i+1]
            if c=="u":
                try: out.append(chr(int(s[i+2:i+6],16))); i+=6; continue
                except: pass
            out.append(c); i+=2
        else:
            out.append(s[i]); i+=1
    return "".join(out)

def entries(html):
    data = ivd(html)
    res=[]
    for m in ENTRY.finditer(data):
        fid,par,name,mime=m.groups()
        res.append((fid, deesc(name), mime))
    return res

root_html = open(os.path.join(os.path.dirname(__file__),"folder.html"),encoding="utf-8",errors="replace").read()
folders = [(fid,name) for fid,name,mime in entries(root_html) if "folder" in mime]
print("subfolders found:", len(folders))

name2id = {}
report = []
for fid,fname in sorted(folders, key=lambda x:x[1]):
    html = fetch(fid)
    ents = [e for e in entries(html) if "folder" not in e[2]]
    for efid,ename,emime in ents:
        name2id[ename] = efid
    report.append((fname, len(ents)))
    print("  %-55s %3d files" % (fname[:55], len(ents)))
    time.sleep(1)

json.dump(name2id, open(os.path.join(os.path.dirname(__file__),"drive_links.json"),"w",encoding="utf-8"),
          ensure_ascii=False, indent=0)
print("TOTAL files mapped:", len(name2id))

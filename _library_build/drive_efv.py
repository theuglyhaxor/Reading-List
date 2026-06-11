# -*- coding: utf-8 -*-
"""Collect file ids using Drive's embeddedfolderview (flat HTML list, no 50-cap)."""
import re, json, subprocess, os, time, html as htmlmod
D = os.path.dirname(__file__)
HDR = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

root = open(os.path.join(D,"folder.html"), encoding="utf-8", errors="replace").read()
raw = re.search(r"_DRIVE_ivd'\] = '(.*?)';", root, re.S).group(1)
raw = re.sub(r"\\x([0-9a-fA-F]{2})", lambda m: chr(int(m.group(1),16)), raw).replace("\\/","/")
FOL = re.compile(r'\["([A-Za-z0-9_-]{20,})",\["[A-Za-z0-9_-]{20,}"\],"((?:[^"\\]|\\.)*?)","application/vnd\.google-apps\.folder"')
folders = [(i,n) for i,n in FOL.findall(raw)]

# embeddedfolderview entries: <div class="flip-entry" id="entry-FILEID"> ... <div class="flip-entry-title">NAME</div>
ENTRY = re.compile(r'id="entry-([A-Za-z0-9_-]{20,})".*?flip-entry-title">(.*?)</div>', re.S)

def efv(fid):
    url = "https://drive.google.com/embeddedfolderview?id=%s#list" % fid
    h = subprocess.run(["curl","-sL","-A",HDR,url], capture_output=True).stdout.decode("utf-8","replace")
    res = {}
    for m in ENTRY.finditer(h):
        fid2, name = m.groups()
        res[htmlmod.unescape(name).strip()] = fid2
    return res, len(h)

name2id = {}
for fid,fname in sorted(folders, key=lambda x:x[1]):
    fl, blen = efv(fid)
    name2id.update(fl)
    print("  %-50s %3d files  (%d bytes)" % (fname[:50], len(fl), blen))
    time.sleep(0.5)

print("TOTAL via efv:", len(name2id))
if len(name2id) >= 380:
    json.dump(name2id, open(os.path.join(D,"drive_links.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=0)
    print("SAVED drive_links.json")
else:
    print("too few, not saving")

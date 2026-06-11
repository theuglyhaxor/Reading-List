# -*- coding: utf-8 -*-
import os, re, json, shutil
BASE=r"d:/READING/Books"
CATS={1:"01 - Marxist and Critical Theory Classics",9:"09 - Political Economy and Globalization"}

# delete confirmed duplicate
dup=os.path.join(BASE,"ধর্ম প্রসঙ্গে - লেনিন.pdf")
if os.path.exists(dup):
    os.remove(dup); print("deleted duplicate:", os.path.basename(dup))

# (filename_in_root, cat, title, lang, genre, pages, summary)
NEW=[
("ছোটদের-রাজনীতি-ও-অর্থনীতি.pdf",9,"ছোটদের রাজনীতি ও অর্থনীতি (Politics and Economics for Young Readers)","Bengali","Political primer",207,
 "An accessible Bengali primer that introduces the basics of politics and economics from a left perspective, written plainly for younger or first-time readers - a gentle on-ramp to the heavier theory on the other shelves."),
("প্রগতি প্রকাশনা_ পরিবার ব্যক্তিগত মালিকানা এবং রাষ্ট্রের উৎপত্তি- ফ্রিডরিখ অ্যাঙ্গেলস .pdf",1,"পরিবার, ব্যক্তিগত মালিকানা ও রাষ্ট্রের উৎপত্তি - ফ্রিডরিখ এঙ্গেলস (The Origin of the Family, Private Property and the State)","Bengali","Marxist theory",218,
 "Bengali edition (Progoti Prokashoni) of Engels's classic tracing how class society, the patriarchal family and the state all arose from changes in property and the mode of production - a cornerstone of Marxist anthropology and feminism."),
("মজুরী-শ্রম ও পুঁজি - মার্কস.pdf",1,"মজুরি-শ্রম ও পুঁজি - কার্ল মার্কস (Wage Labour and Capital)","Bengali","Marxist theory",35,
 "Bengali translation of Marx's short, lucid lectures explaining wages, labour-power, exploitation and capital in everyday terms - one of the easiest doors into his economics, ideal before tackling Capital."),
("সমাজন্ত্র কেন_.pdf",1,"সমাজতন্ত্র কেন? (Why Socialism?)","Bengali","Essay",18,
 "A short Bengali pamphlet that argues, in plain language, why socialism answers the failures of capitalism - a quick, persuasive read for newcomers to the idea."),
("সাম্রাজ্যবাদ-পুঁজিবাদের-সর্বোচ্চ-পর্যায়-মূল-লেখা-ও-সুচি.pdf",1,"সাম্রাজ্যবাদ - পুঁজিবাদের সর্বোচ্চ পর্যায় - লেনিন (মূল লেখা ও সূচিসহ সংস্করণ)","Bengali","Marxist theory",59,
 "Bengali edition of Lenin's Imperialism, the Highest Stage of Capitalism, carrying the full core text with contents - his account of how monopoly, finance capital and the carve-up of the world turn capitalism into imperialism."),
]

def san(name):
    name=name.replace(":"," -").replace("/"," ").replace("\\"," ")
    name=re.sub(r'[*?"<>|]',"",name); name=re.sub(r"\s+"," ",name).strip().strip(".")
    return name[:145].rstrip() if len(name)>145 else name

cr=json.load(open(r"d:/READING/_library_build/catalog_result.json","r",encoding="utf-8"))
records=cr["records"]
existing_titles={r[1] for r in records}
added=0
for fn,cat,title,lang,genre,pages,summ in NEW:
    src=os.path.join(BASE,fn)
    if not os.path.exists(src):
        print("MISSING:",fn); continue
    if title in existing_titles:
        print("already present, skip:",title); continue
    dstdir=os.path.join(BASE,CATS[cat]); os.makedirs(dstdir,exist_ok=True)
    dst=os.path.join(dstdir,san(title)+".pdf")
    n=2
    while os.path.exists(dst):
        dst=os.path.join(dstdir,san(title)+(" (%d)"%n)+".pdf"); n+=1
    shutil.move(src,dst)
    newrel=os.path.relpath(dst,BASE).replace(os.sep,"/")
    records.append([cat,title,lang,genre,summ,newrel,pages]); added+=1
    print("added:",newrel)

json.dump(cr,open(r"d:/READING/_library_build/catalog_result.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ADDED",added,"-> total non-dup records:",len([r for r in records if r[0]!=99]))

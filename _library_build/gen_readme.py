# -*- coding: utf-8 -*-
import json, urllib.parse, os, unicodedata
from collections import Counter
def _nfc(s): return unicodedata.normalize("NFC", s)
DRIVE = {_nfc(k):v for k,v in json.load(open(r"d:/READING/_library_build/drive_links.json","r",encoding="utf-8")).items()}

cr = json.load(open(r"d:/READING/_library_build/catalog_result.json","r",encoding="utf-8"))
recs = [r for r in cr["records"] if r[0] != 99]   # cat,title,lang,genre,summary,newrel,pages

CATS = {
 1:"01 - Marxist and Critical Theory Classics", 2:"02 - Marx-Engels Collected Works (MECW)",
 3:"03 - Maoism and Peoples War", 4:"04 - Indian Communist and Naxalite Movement",
 5:"05 - Caste, Dalit and Social Justice", 6:"06 - Kashmir", 7:"07 - Palestine and West Asia",
 8:"08 - History, State and Politics", 9:"09 - Political Economy and Globalization",
 10:"10 - Ecology, Science and Society", 11:"11 - Literature and the Arts",
 12:"12 - Biography and Memoir", 13:"13 - Bangladesh - History and Politics",
 14:"14 - Feminism and Gender", 15:"15 - Cybersecurity and Hacking",
 16:"16 - Periodicals, Pamphlets and Reports",
}
CATS_BN = {
 1:"০১ - মার্কসবাদী ও সমালোচনামূলক তত্ত্বের ক্লাসিক", 2:"০২ - মার্ক্স-এঙ্গেলস রচনাসমগ্র (MECW)",
 3:"০৩ - মাওবাদ ও জনযুদ্ধ", 4:"০৪ - ভারতীয় কমিউনিস্ট ও নকশাল আন্দোলন",
 5:"০৫ - জাতপাত, দলিত ও সামাজিক ন্যায়", 6:"০৬ - কাশ্মীর", 7:"০৭ - প্যালেস্টাইন ও পশ্চিম এশিয়া",
 8:"০৮ - ইতিহাস, রাষ্ট্র ও রাজনীতি", 9:"০৯ - রাজনৈতিক অর্থনীতি ও বিশ্বায়ন",
 10:"১০ - বাস্তুতন্ত্র, বিজ্ঞান ও সমাজ", 11:"১১ - সাহিত্য ও শিল্পকলা",
 12:"১২ - জীবনী ও স্মৃতিকথা", 13:"১৩ - বাংলাদেশ - ইতিহাস ও রাজনীতি",
 14:"১৪ - নারীবাদ ও লিঙ্গ", 15:"১৫ - সাইবার নিরাপত্তা ও হ্যাকিং",
 16:"১৬ - সাময়িকী, পুস্তিকা ও প্রতিবেদন",
}
TAG = {
 1:"Marx, Engels, Lenin, Mao & critical theory - the bedrock",
 2:"The 50-volume Collected Works (incl. *Capital* I-III)",
 3:"Mao, people's war and the modern MLM tradition",
 4:"Naxalbari to Dandakaranya - India's Maoist movement",
 5:"Caste, Dalit history and anti-caste theory",
 6:"Kashmir - chronicles, nationalism, human rights",
 7:"Palestine - history, programme, literature of exile",
 8:"Wide-angle history, politics, media, law & the state",
 9:"Capitalism, imperialism, debt and the Indian economy",
 10:"Ecology, philosophy of science and rationalism",
 11:"Fiction, poetry, song, theatre - Bengali & world",
 12:"Memoirs and biographies of revolutionaries",
 13:"East Bengal/Bangladesh - 1952, 1971, Bhashani, Sikder",
 14:"Women in revolution and the theory of liberation",
 15:"Ethical hacking, pen-testing & the dark web (standalone)",
 16:"Magazines, bulletins, pamphlets and official reports",
}
TAG_BN = {
 1:"মার্ক্স, এঙ্গেলস, লেনিন, মাও ও সমালোচনামূলক তত্ত্ব - ভিত্তি",
 2:"৫০ খণ্ডের রচনাসমগ্র (*ক্যাপিটাল* ১-৩ সহ)",
 3:"মাও, জনযুদ্ধ ও আধুনিক এমএলএম ধারা",
 4:"নকশালবাড়ি থেকে দণ্ডকারণ্য - ভারতের মাওবাদী আন্দোলন",
 5:"জাতপাত, দলিত ইতিহাস ও জাতপাত-বিরোধী তত্ত্ব",
 6:"কাশ্মীর - ইতিহাস, জাতীয়তাবাদ, মানবাধিকার",
 7:"প্যালেস্টাইন - ইতিহাস, কর্মসূচি, নির্বাসনের সাহিত্য",
 8:"বিস্তৃত ইতিহাস, রাজনীতি, মিডিয়া, আইন ও রাষ্ট্র",
 9:"পুঁজিবাদ, সাম্রাজ্যবাদ, ঋণ ও ভারতীয় অর্থনীতি",
 10:"বাস্তুতন্ত্র, বিজ্ঞানের দর্শন ও যুক্তিবাদ",
 11:"কথাসাহিত্য, কবিতা, গান, নাটক - বাংলা ও বিশ্ব",
 12:"বিপ্লবীদের স্মৃতিকথা ও জীবনী",
 13:"পূর্ববঙ্গ/বাংলাদেশ - ১৯৫২, ১৯৭১, ভাসানী, সিকদার",
 14:"বিপ্লবে নারী ও মুক্তির তত্ত্ব",
 15:"নৈতিক হ্যাকিং, পেন-টেস্টিং ও ডার্ক ওয়েব (স্বতন্ত্র)",
 16:"পত্রিকা, বুলেটিন, পুস্তিকা ও সরকারি প্রতিবেদন",
}
BLURB = {
 1:"The bedrock - Marx, Engels, Lenin, Stalin and Mao in their own words, plus the philosophy and political economy that frame everything else in the library.",
 2:"The complete 50-volume Lawrence and Wishart *Collected Works of Marx and Engels* - a reference shelf. Volumes 35-37 are *Capital* I-III.",
 3:"Mao Zedong, the theory of people's war, and the modern Maoist (MLM) tradition from China to the Philippines, Turkey and Peru.",
 4:"The Indian communist and Naxalite/Maoist movement - from the 1948 thesis and Naxalbari to Dandakaranya, told through history, reportage and party documents.",
 5:"Caste as the axis of Indian social oppression - Dalit history, anti-caste theory and first-person testimony.",
 6:"Kashmir - its classical chronicles, its nationalism, and the human-rights literature of the conflict.",
 7:"Palestine and West Asia - history, political programme and the literature of exile.",
 8:"Wide-angle history and politics - India and the world, communalism, media, law and the state.",
 9:"How capitalism and imperialism actually work - debt, neoliberalism, the Indian economy and the global order.",
 10:"Ecology, the history and philosophy of science, and rationalism - the natural world and how we know it.",
 11:"Fiction, poetry, song, theatre and literary study - mostly Bengali, with world classics in translation.",
 12:"Lives - memoirs and biographies of revolutionaries, prisoners and witnesses.",
 13:"Bangladesh / East Bengal - the Language Movement, the 1971 Liberation War, Bhashani and Siraj Sikder.",
 14:"Feminism and gender - women in revolutionary movements and the theory of women's liberation.",
 15:"A self-contained technical shelf - ethical hacking, penetration testing, Android and API security, and the dark web.",
 16:"Magazines, bulletins, pamphlets and official reports - the periodical literature of the movements above.",
}
BLURB_BN = {
 1:"ভিত্তি - মার্ক্স, এঙ্গেলস, লেনিন, স্ট্যালিন ও মাও তাঁদের নিজের ভাষায়, সঙ্গে দর্শন ও রাজনৈতিক অর্থনীতি।",
 2:"ল্যরেন্স অ্যান্ড উইশার্টের সম্পূর্ণ ৫০ খণ্ডের *মার্ক্স-এঙ্গেলস রচনাসমগ্র* - রেফারেন্স তাক। ৩৫-৩৭ খণ্ড *ক্যাপিটাল* ১-৩।",
 3:"মাও সে-তুং, জনযুদ্ধের তত্ত্ব এবং চীন থেকে ফিলিপাইন, তুরস্ক ও পেরু পর্যন্ত আধুনিক মাওবাদী (এমএলএম) ধারা।",
 4:"ভারতের কমিউনিস্ট ও নকশাল/মাওবাদী আন্দোলন - ১৯৪৮-এর থিসিস ও নকশালবাড়ি থেকে দণ্ডকারণ্য পর্যন্ত।",
 5:"ভারতীয় সামাজিক নিপীড়নের অক্ষ হিসেবে জাতপাত - দলিত ইতিহাস, তত্ত্ব ও আত্মকথন।",
 6:"কাশ্মীর - এর প্রাচীন ইতিহাস, জাতীয়তাবাদ ও সংঘাতের মানবাধিকার সাহিত্য।",
 7:"প্যালেস্টাইন ও পশ্চিম এশিয়া - ইতিহাস, রাজনৈতিক কর্মসূচি ও নির্বাসনের সাহিত্য।",
 8:"বিস্তৃত ইতিহাস ও রাজনীতি - ভারত ও বিশ্ব, সাম্প্রদায়িকতা, মিডিয়া, আইন ও রাষ্ট্র।",
 9:"পুঁজিবাদ ও সাম্রাজ্যবাদ কীভাবে কাজ করে - ঋণ, নয়া-উদারবাদ, ভারতীয় অর্থনীতি ও বিশ্বব্যবস্থা।",
 10:"বাস্তুতন্ত্র, বিজ্ঞানের ইতিহাস ও দর্শন, এবং যুক্তিবাদ - প্রকৃতি ও আমাদের জ্ঞান।",
 11:"কথাসাহিত্য, কবিতা, গান, নাটক ও সাহিত্য-আলোচনা - বেশিরভাগ বাংলা, সঙ্গে বিশ্বক্লাসিকের অনুবাদ।",
 12:"জীবন - বিপ্লবী, বন্দি ও সাক্ষীদের স্মৃতিকথা ও জীবনী।",
 13:"বাংলাদেশ / পূর্ববঙ্গ - ভাষা আন্দোলন, ১৯৭১-এর মুক্তিযুদ্ধ, ভাসানী ও সিরাজ সিকদার।",
 14:"নারীবাদ ও লিঙ্গ - বিপ্লবী আন্দোলনে নারী এবং নারীমুক্তির তত্ত্ব।",
 15:"একটি স্বতন্ত্র কারিগরি তাক - নৈতিক হ্যাকিং, পেনিট্রেশন টেস্টিং, অ্যান্ড্রয়েড ও এপিআই নিরাপত্তা, ডার্ক ওয়েব।",
 16:"পত্রিকা, বুলেটিন, পুস্তিকা ও সরকারি প্রতিবেদন - উপরের আন্দোলনগুলোর সাময়িক সাহিত্য।",
}

# ---------- difficulty level ----------
ADV = {"Marxist theory","Political theory","Philosophy","Philosophy of science","Anti-colonial theory",
 "Feminist theory","Caste studies","Eco-Marxism","Social ecology","Political economy","International relations"}
BEG = {"Novel","Novels","Short story","Short stories","Poetry","Poetry anthology","Songs","Songs and lyrics",
 "Song","Fiction","Historical fiction","Self-help","Rationalism","Sport and essays","Memoir","Children",
 "Anthology","Pamphlet","Magazine","Periodical","Bulletin","Report","Miscellany","Technology",
 "True crime and tech","Political primer","Gender","Memoir and Children"}
LVL_OVERRIDE = {  # title substring -> level
 "Hacking - Computer Hacking":"Beginner","Beginning Ethical Hacking":"Beginner",
 "The Basics of Hacking":"Beginner","Hacking Wireless Networks for Dummies":"Beginner",
 "The Surface, Deep and Dark Web":"Beginner","The Dark Web for the Rational":"Beginner",
 "The Dark Secrets of the Search Engines":"Beginner","The Darkest Web":"Beginner",
 "The Anarchist Cookbook":"Beginner","Penetration Testing - A Hands-On":"Intermediate",
 "Hacking APIs":"Intermediate","Black Hat GraphQL":"Advanced","Android Security Internals":"Advanced",
 "Android Hacker's Handbook":"Advanced","The Android Malware Handbook":"Advanced",
 "The Hardware Hacking Handbook":"Advanced","From Day Zero to Zero Day":"Advanced",
 "Communist Manifesto":"Beginner","Marxist Political Economy - An Introductory":"Beginner",
 "Wage Labour and Capital":"Beginner","মজুরি-শ্রম":"Beginner","Why Socialism":"Beginner",
 "সমাজতন্ত্র কেন":"Beginner","Politics and Economics for Young":"Beginner","ছোটদের রাজনীতি":"Beginner",
 "Marxism-Leninism-Maoism Basic Course":"Beginner","Basic Principles of Marxism-Leninism":"Beginner",
 "Activist Study":"Beginner","মাও রেডবুক":"Beginner","Quotations from Chairman Mao":"Beginner",
 "The Origin of the Family":"Intermediate","পরিবার, ব্যক্তিগত":"Intermediate",
 "Subimal Misra":"Advanced","সুবিমল মিশ্র":"Advanced","Akhtaruzzaman Elias":"Advanced",
 "আখতারুজ্জামান":"Advanced","Grundrisse":"Advanced","Capital, Volume III":"Advanced",
 "Unidentified":"-","Babar":"-","বাবর":"-","Bajol Bheri":"-","বাজল ভেরী":"-",
 "Lal Tomsuk":"-","লাল তমসুক":"-",
}
def level(cat, genre, title):
    if cat == 2: return "Reference"
    for k,v in LVL_OVERRIDE.items():
        if k in title: return v
    if genre in ADV: return "Advanced"
    if genre in BEG: return "Beginner"
    return "Intermediate"

LVL_BN = {"Beginner":"প্রাথমিক","Intermediate":"মধ্যম","Advanced":"উন্নত","Reference":"রেফারেন্স","-":"—"}
LANG_BN = {"English":"ইংরেজি","Bengali":"বাংলা"}

# ---------- three reading maps ----------
POL_MAP = [
"```mermaid","flowchart TD",
'    START([" START HERE "]):::s',
'    START --> F["1. FOUNDATIONS · Shelf 01<br/><i>Communist Manifesto → Wage Labour &amp; Capital<br/>→ Fanon, Wretched of the Earth</i>"]:::a',
'    F --> PE["2. POLITICAL ECONOMY · Shelf 01→09→02<br/><i>Marxist Pol-Econ Intro → Imperialism (Lenin)<br/>→ Capital I–III</i>"]:::a',
'    PE --> METHOD["3. METHOD / MAOISM · Shelf 03<br/><i>MLM Basic Course → On New Democracy<br/>→ On Practice &amp; Contradiction</i>"]:::a',
'    METHOD --> Q{"4. APPLY IT:<br/>which struggle?"}:::q',
'    Q --> NAX["NAXALITE MOVEMENT · 04<br/><i>India After Naxalbari →<br/>Jangalnama → Janatana State</i>"]:::b',
'    Q --> ECON["INDIAN ECONOMY · 09<br/><i>Working Class → Semi-Feudal<br/>debate → Crisis &amp; Predation</i>"]:::b',
'    Q --> CASTE["CASTE &amp; DALIT · 05<br/><i>Republic of Caste →<br/>Critiquing Brahmanism</i>"]:::b',
'    Q --> REGION["REGIONAL / GLOBAL<br/>Kashmir 06 · Palestine 07 ·<br/>Bangladesh 13"]:::b',
'    NAX --> CTX["5. CONTEXT &amp; DEPTH"]:::c',
'    ECON --> CTX',
'    CASTE --> CTX',
'    REGION --> CTX',
'    CTX --> H["HISTORY &amp; STATE · 08"]:::c',
'    CTX --> ECO["ECOLOGY &amp; SCIENCE · 10"]:::c',
'    CTX --> FEM["FEMINISM &amp; GENDER · 14"]:::c',
'    CTX --> BIO["BIOGRAPHY &amp; MEMOIR · 12"]:::c',
'    H --> REF["REFERENCE<br/>MECW Shelf 02 ·<br/>Periodicals Shelf 16"]:::d',
"    classDef s fill:#b71c1c,stroke:#000,color:#fff;",
"    classDef a fill:#e53935,stroke:#000,color:#fff;",
"    classDef q fill:#6a1b9a,stroke:#000,color:#fff;",
"    classDef b fill:#1565c0,stroke:#000,color:#fff;",
"    classDef c fill:#2e7d32,stroke:#000,color:#fff;",
"    classDef d fill:#5d4037,stroke:#000,color:#fff;",
"```",
]
CYB_MAP = [
"```mermaid","flowchart TD",
'    S([" Beginner<br/>START HERE "]):::s',
'    S --> A1["1. Hacking - Computer Hacking,<br/>Security &amp; Pen-Testing (Gary Hall)<br/><i>plain-English overview</i>"]:::a',
'    A1 --> A2["2. Beginning Ethical Hacking<br/>with Kali Linux (Sanjib Sinha)<br/><i>build your lab</i>"]:::a',
'    A2 --> A3["3. The Basics of Hacking and<br/>Penetration Testing (Engebretson)<br/><i>the methodology</i>"]:::a',
'    A3 --> A4["4. Penetration Testing - A Hands-On<br/>Introduction (Georgia Weidman)<br/><i>full hands-on course</i>"]:::a',
'    A4 --> PICK{"Now pick a<br/>specialty"}:::q',
'    PICK --> WEB["WEB &amp; APIs · intermediate→adv<br/>Hacking APIs (Ball) →<br/>Black Hat GraphQL"]:::b',
'    PICK --> WIFI["WIRELESS · beginner<br/>Hacking Wireless<br/>Networks for Dummies"]:::b',
'    PICK --> MOB["MOBILE / ANDROID · advanced<br/>Android Security Internals →<br/>Android Hacker&#39;s Handbook →<br/>The Android Malware Handbook"]:::b',
'    PICK --> HW["HARDWARE · advanced<br/>The Hardware<br/>Hacking Handbook"]:::b',
'    WEB --> ADV["CAPSTONE · advanced<br/>From Day Zero to Zero Day<br/><i>find your own 0-days</i>"]:::c',
'    MOB --> ADV',
'    HW --> ADV',
'    DARK["DARK-WEB AWARENESS · read any time, non-technical<br/>Surface / Deep / Dark Web → The Dark Web for the Rational →<br/>The Dark Secrets of Search Engines → The Darkest Web"]:::e',
'    CURIO["The Anarchist Cookbook — historical curio only, not a syllabus"]:::g',
'    S -.->|"context / awareness"| DARK',
"    classDef s fill:#b71c1c,stroke:#000,color:#fff;",
"    classDef a fill:#37474f,stroke:#000,color:#fff;",
"    classDef q fill:#6a1b9a,stroke:#000,color:#fff;",
"    classDef b fill:#1565c0,stroke:#000,color:#fff;",
"    classDef c fill:#2e7d32,stroke:#000,color:#fff;",
"    classDef e fill:#455a64,stroke:#000,color:#fff;",
"    classDef g fill:#5d4037,stroke:#000,color:#fff;",
"```",
]
LIT_MAP = [
"```mermaid","flowchart TD",
'    S([" New reader<br/>START HERE "]):::s',
'    S --> EASY["1. THE EASY WAY IN · beginner<br/><i>Totto-chan</i> (memoir) ·<br/><i>Animal Farm</i> (Bangla) ·<br/><i>Soccer in Sun and Shadow</i>"]:::a',
'    EASY --> SHORT["2. SHORT STORIES · beginner<br/><i>Best 100 of O. Henry</i> →<br/><i>Best Urdu Stories</i> →<br/><i>Draupadi</i> (Mahasweta Devi)"]:::a',
'    SHORT --> NOV["3. NOVELS · intermediate<br/><i>Mother</i> (Gorky) →<br/>Best Novels of Manik Bandyopadhyay →<br/><i>From Volga to Ganga</i>"]:::a',
'    NOV --> HARD["4. ADVANCED / EXPERIMENTAL<br/>Akhtaruzzaman Elias (Collected) →<br/>Subimal Misra Anti-Stories 1, 3, 4"]:::d',
'    S --> POE["POETRY TRACK · beginner→int<br/>Sukanta Samagra →<br/>Birendra Chattopadhyay →<br/>Subhash Mukhopadhyay →<br/>Bengali Poetry Anthology (Sukumar Sen)"]:::b',
'    S --> SONG["SONG &amp; MUSIC · beginner<br/>Sumaner Gaan (Kabir Suman) ·<br/>Kon Pothe Gelo Gaan ·<br/>Songs of Revolution"]:::c',
'    S --> CRAFT["CRAFT &amp; STUDY · intermediate<br/>Creating a Role (Stanislavski) +<br/>An Actor&#39;s Rebirth I–II ·<br/>Jhumur O Charyapad (study)"]:::c',
"    classDef s fill:#4a148c,stroke:#000,color:#fff;",
"    classDef a fill:#6a1b9a,stroke:#000,color:#fff;",
"    classDef b fill:#00695c,stroke:#000,color:#fff;",
"    classDef c fill:#1565c0,stroke:#000,color:#fff;",
"    classDef d fill:#ad1457,stroke:#000,color:#fff;",
"```",
]

DRIVE_URL = "https://drive.google.com/drive/folders/1kIpTbRnVZQIO8AFEYrJ9ySVf8qcGhFAc?usp=sharing"

def anchor(s):
    a = "".join(ch if (ch.isalnum() or ch==" ") else "" for ch in s.lower()).strip()
    return a.replace(" ","-")
def link(rel):
    fid = DRIVE.get(_nfc(os.path.basename(rel)))
    if fid:
        return "https://drive.google.com/file/d/%s/view?usp=sharing" % fid
    return DRIVE_URL  # fallback: the shared folder

total = len(recs)
langs = Counter(r[2] for r in recs)
bycat = Counter(r[0] for r in recs)
levels = Counter(level(r[0],r[3],r[1]) for r in recs)

# ===================== ENGLISH =====================
def build_en():
    o=[]; A=o.append
    A("# The Reading Room — A Working Library")
    A("")
    A("A curated digital library of **%d PDF books, pamphlets and periodicals** on Marxism, the Indian and Bangladeshi communist and Naxalite movements, caste, Kashmir, Palestine, history, political economy, ecology, Bengali and world literature — plus a self-contained cybersecurity shelf." % total)
    A("")
    A("Every file is renamed to its real title, sorted into a numbered subject shelf, tagged with a **reading level**, and given a one-line summary. **A Bengali version of this page is at [README.bn.md](README.bn.md).**")
    A("")
    A("> ## 📥 Download the books")
    A("> The PDFs are too large for GitHub (~6.5 GB), so the whole library is hosted on **Google Drive, open to everyone**:")
    A("> ")
    A("> ### ➤ **[Open the library on Google Drive](%s)**" % DRIVE_URL)
    A("> ")
    A("> **Every book title in the catalogue below links straight to its PDF on Google Drive** — click a title to open or download that single book, or use the folder link above to grab everything at once.")
    A("")
    A("**Languages:** %s &nbsp;•&nbsp; **Levels:** %s" % (
        ", ".join("%d %s" % (c,l) for l,c in langs.most_common()),
        ", ".join("%d %s" % (levels[k],k) for k in ["Beginner","Intermediate","Advanced","Reference"] if levels.get(k))))
    A("")
    A("> Most works lean left/radical and many are scanned activist editions; *(parentheses)* give the English title of a Bengali book. A few image-only scans had no metadata and are labelled honestly as *Unidentified*.")
    A("")
    A("**Reading-level key** — 🟢 **Beginner** (no background needed) · 🟡 **Intermediate** (some grounding helps) · 🔴 **Advanced** (dense / scholarly) · 📘 **Reference** (look things up, don't read cover-to-cover).")
    A(""); A("---"); A("")
    # overview
    A("## The shelves")
    A("")
    A("| # | Shelf | Items | What's on it |")
    A("|---|-------|------:|--------------|")
    for k in range(1,17):
        if bycat.get(k):
            A("| %02d | [%s](#%s) | %d | %s |" % (k, CATS[k].split(' - ',1)[1], anchor(CATS[k]), bycat[k], TAG[k]))
    A(""); A("---"); A("")
    # reading maps
    A("## Reading maps — where to start")
    A("")
    A("Three independent routes through the library. Follow the numbered spine of whichever one calls you; the side-branches are optional specialisms you can take in any order.")
    A("")
    A("### 🚩 Map 1 — Politics, Theory & History")
    A("")
    A("The main current of the collection. Start with the **Foundations**, get the **method**, then follow a **struggle**, then widen into **context**.")
    A(""); o += POL_MAP; A("")
    A("### 🔐 Map 2 — Cybersecurity & Hacking")
    A("")
    A("A standalone technical track. Climb the numbered spine (overview → lab → method → hands-on course), **then** pick a specialty. The dark-web titles are non-technical awareness reading.")
    A(""); o += CYB_MAP; A("")
    A("### 📖 Map 3 — Literature & the Arts")
    A("")
    A("Read down the middle spine (easy → short stories → novels → experimental), and dip into the Poetry, Song and Craft side-tracks whenever you like.")
    A(""); o += LIT_MAP; A("")
    A("> *Note:* the four *Unidentified Bengali Volume* scans and a few one-word titles (*Babar*, *Bajol Bheri*, *Lal Tomsuk*) sit outside the literature map until their contents are confirmed.")
    A(""); A("---"); A("")
    # catalogue
    A("## The catalogue")
    A("")
    A("Each shelf lists its books with **Level**, **Genre**, **Pages** and a **Summary** of what the book actually contains. Titles are clickable.")
    A("")
    EMO={"Beginner":"🟢","Intermediate":"🟡","Advanced":"🔴","Reference":"📘","-":"⚪"}
    for k in range(1,17):
        items=[r for r in recs if r[0]==k]
        if not items: continue
        items.sort(key=lambda r:r[5].lower())
        A("### %s" % CATS[k]); A(""); A("*%s*" % BLURB[k]); A("")
        A("| # | Title | Lang | Level | Genre | Pages | Summary |")
        A("|--:|-------|------|-------|-------|------:|---------|")
        for i,(cat,title,lang,genre,summ,rel,pages) in enumerate(items,1):
            lv=level(cat,genre,title)
            A("| %d | [%s](%s) | %s | %s %s | %s | %s | %s |" % (
                i, title.replace("|","/"), link(rel), lang, EMO[lv], lv,
                genre, pages or "", summ.replace("|","/")))
        A("")
    A("---"); A("")
    A("## Notes")
    A("")
    A("- The catalogue is **generated from data**, so titles, links and counts always match what is on disk.")
    A("- **Duplicates have been removed** — every title here is unique.")
    A("- A few files are **encrypted or image-only scans** with no extractable text; these are catalogued from their filenames and flagged in the summary.")
    A("- **Reading levels are a guide, not a gate** — read whatever grabs you.")
    A(""); A("---"); A("")
    A(ABOUT_EN); A(""); A("---"); A(""); A(SOCIAL)
    return "\n".join(o)+"\n"

# ===================== BENGALI =====================
def build_bn():
    o=[]; A=o.append
    A("# পাঠশালা — একটি চলমান গ্রন্থাগার")
    A("")
    A("মার্কসবাদ, ভারত ও বাংলাদেশের কমিউনিস্ট ও নকশাল আন্দোলন, জাতপাত, কাশ্মীর, প্যালেস্টাইন, ইতিহাস, রাজনৈতিক অর্থনীতি, বাস্তুতন্ত্র, বাংলা ও বিশ্বসাহিত্য — এবং একটি স্বতন্ত্র সাইবার-নিরাপত্তা তাক নিয়ে সাজানো **%d টি পিডিএফ বই, পুস্তিকা ও পত্রিকার** একটি গ্রন্থাগার।" % total)
    A("")
    A("প্রতিটি ফাইলকে এর প্রকৃত শিরোনামে নতুন নাম দেওয়া হয়েছে, বিষয়ভিত্তিক তাকে সাজানো হয়েছে, একটি **পাঠ-স্তর** দেওয়া হয়েছে এবং সংক্ষিপ্ত সারসংক্ষেপ যোগ করা হয়েছে। **এই পাতার ইংরেজি সংস্করণ: [README.md](README.md)।**")
    A("")
    A("> ## 📥 বইগুলো ডাউনলোড করুন")
    A("> ফাইলগুলো GitHub-এর জন্য অনেক বড় (~৬.৫ গিগাবাইট), তাই পুরো গ্রন্থাগারটি **Google Drive-এ সবার জন্য উন্মুক্ত** রাখা হয়েছে:")
    A("> ")
    A("> ### ➤ **[Google Drive-এ গ্রন্থাগার খুলুন](%s)**" % DRIVE_URL)
    A("> ")
    A("> **নিচের তালিকার প্রতিটি বইয়ের শিরোনাম সরাসরি Google Drive-এ সেই PDF-এর সঙ্গে লিঙ্ক করা** — শিরোনামে ক্লিক করলেই বইটি খুলবে বা নামানো যাবে; অথবা উপরের ফোল্ডার লিঙ্ক থেকে একসঙ্গে সব নিন।")
    A("")
    A("**ভাষা:** %s &nbsp;•&nbsp; **স্তর:** %s" % (
        ", ".join("%d %s" % (c, LANG_BN.get(l,l)) for l,c in langs.most_common()),
        ", ".join("%d %s" % (levels[k], LVL_BN[k]) for k in ["Beginner","Intermediate","Advanced","Reference"] if levels.get(k))))
    A("")
    A("> বেশিরভাগ বই বামপন্থী/মৌলবাদী ধারার; *(বন্ধনীতে)* বাংলা বইয়ের ইংরেজি শিরোনাম দেওয়া আছে। কিছু স্ক্যান করা ফাইলে কোনো তথ্য না থাকায় সেগুলো সততার সঙ্গে *Unidentified* হিসেবে চিহ্নিত।")
    A("")
    A("> **নোট:** বইয়ের সারসংক্ষেপগুলো আপাতত ইংরেজিতে রাখা হয়েছে; বাকি সব নির্দেশনা বাংলায়।")
    A("")
    A("**পাঠ-স্তর সংকেত** — 🟢 **প্রাথমিক** (কোনো পূর্বজ্ঞান লাগে না) · 🟡 **মধ্যম** (সামান্য প্রস্তুতি কাজে দেয়) · 🔴 **উন্নত** (জটিল / পাণ্ডিত্যপূর্ণ) · 📘 **রেফারেন্স** (খুঁজে দেখার জন্য, শুরু-থেকে-শেষ পড়ার জন্য নয়)।")
    A(""); A("---"); A("")
    A("## তাকসমূহ")
    A("")
    A("| # | তাক | সংখ্যা | কী আছে |")
    A("|---|-----|------:|--------|")
    for k in range(1,17):
        if bycat.get(k):
            A("| %02d | [%s](#%s) | %d | %s |" % (k, CATS_BN[k].split(' - ',1)[1], anchor(CATS_BN[k]), bycat[k], TAG_BN[k]))
    A(""); A("---"); A("")
    A("## পাঠ-মানচিত্র — কোথা থেকে শুরু করবেন")
    A("")
    A("গ্রন্থাগারে চলার তিনটি স্বতন্ত্র পথ। যেটি আপনাকে টানে তার সংখ্যাযুক্ত মূল ধারা অনুসরণ করুন; পাশের শাখাগুলো ঐচ্ছিক, যেকোনো ক্রমে পড়তে পারেন। *(মানচিত্রের লেখা ইংরেজিতে, কারণ বইয়ের শিরোনামও ইংরেজিতে।)*")
    A("")
    A("### 🚩 মানচিত্র ১ — রাজনীতি, তত্ত্ব ও ইতিহাস")
    A("")
    A("সংগ্রহের মূল স্রোত। **ভিত্তি** দিয়ে শুরু করুন, **পদ্ধতি** আয়ত্ত করুন, তারপর একটি **সংগ্রাম** বেছে নিন, এরপর **প্রেক্ষাপটে** ছড়িয়ে পড়ুন।")
    A(""); o += POL_MAP; A("")
    A("### 🔐 মানচিত্র ২ — সাইবার নিরাপত্তা ও হ্যাকিং")
    A("")
    A("একটি স্বতন্ত্র কারিগরি পথ। সংখ্যাযুক্ত ধারা বেয়ে উঠুন (পরিচিতি → ল্যাব → পদ্ধতি → হাতে-কলমে কোর্স), **তারপর** একটি বিশেষায়ন বেছে নিন। ডার্ক-ওয়েব বইগুলো অ-কারিগরি সচেতনতামূলক পাঠ।")
    A(""); o += CYB_MAP; A("")
    A("### 📖 মানচিত্র ৩ — সাহিত্য ও শিল্পকলা")
    A("")
    A("মাঝের মূল ধারা ধরে পড়ুন (সহজ → ছোটগল্প → উপন্যাস → পরীক্ষামূলক), আর কবিতা, গান ও শিল্পচর্চার পাশের পথগুলোতে যখন খুশি ঢুঁ মারুন।")
    A(""); o += LIT_MAP; A("")
    A("> *নোট:* চারটি *Unidentified Bengali Volume* স্ক্যান এবং কয়েকটি এক-শব্দের শিরোনাম (*বাবর*, *বাজল ভেরী*, *লাল তমসুক*) বিষয়বস্তু নিশ্চিত না হওয়া পর্যন্ত সাহিত্য-মানচিত্রের বাইরে রাখা হয়েছে।")
    A(""); A("---"); A("")
    A("## গ্রন্থতালিকা")
    A("")
    A("প্রতিটি তাকে বইয়ের সঙ্গে আছে **স্তর**, **ধরন**, **পৃষ্ঠা** এবং বইটিতে আসলে কী আছে তার **সারসংক্ষেপ**। শিরোনামে ক্লিক করলে ফাইল খুলবে।")
    A("")
    EMO={"Beginner":"🟢","Intermediate":"🟡","Advanced":"🔴","Reference":"📘","-":"⚪"}
    for k in range(1,17):
        items=[r for r in recs if r[0]==k]
        if not items: continue
        items.sort(key=lambda r:r[5].lower())
        A("### %s" % CATS_BN[k]); A(""); A("*%s*" % BLURB_BN[k]); A("")
        A("| # | শিরোনাম | ভাষা | স্তর | ধরন | পৃষ্ঠা | সারসংক্ষেপ |")
        A("|--:|---------|------|------|------|------:|-----------|")
        for i,(cat,title,lang,genre,summ,rel,pages) in enumerate(items,1):
            lv=level(cat,genre,title)
            A("| %d | [%s](%s) | %s | %s %s | %s | %s | %s |" % (
                i, title.replace("|","/"), link(rel), LANG_BN.get(lang,lang),
                EMO[lv], LVL_BN[lv], genre, pages or "", summ.replace("|","/")))
        A("")
    A("---"); A("")
    A("## কিছু কথা")
    A("")
    A("- তালিকা **ডেটা থেকে স্বয়ংক্রিয়ভাবে তৈরি**, তাই শিরোনাম, লিঙ্ক ও সংখ্যা সবসময় ডিস্কের সঙ্গে মেলে।")
    A("- **নকল কপি সরিয়ে ফেলা হয়েছে** — প্রতিটি শিরোনাম অনন্য।")
    A("- কয়েকটি ফাইল **এনক্রিপ্টেড বা কেবল ছবি-স্ক্যান**; সেগুলো ফাইলের নাম থেকে তালিকাভুক্ত ও সারসংক্ষেপে চিহ্নিত।")
    A("- **পাঠ-স্তর একটি দিকনির্দেশ মাত্র** — যা আপনাকে টানে, তা-ই পড়ুন।")
    A(""); A("---"); A("")
    A(ABOUT_BN); A(""); A("---"); A(""); A(SOCIAL)
    return "\n".join(o)+"\n"

ABOUT_EN = (
"## About the curator\n\n"
"I'm **theuglyhaxor**. This library grew out of two long-running obsessions — radical politics and history on one side, security research and hacking on the other — and a simple belief that good books should be easy to find and free to read.\n\n"
"What you see here is the shelf I actually read from: Marx and the Marxist tradition, the Indian and Bangladeshi communist and Naxalite movements, caste and Dalit writing, Kashmir and Palestine, Bengali literature, and a working cybersecurity library. I cleaned it up, gave every file its real title, sorted it by subject, tagged reading levels, and drew the maps above so a newcomer can find a way in instead of drowning in a folder of hundreds of PDFs.\n\n"
"If any of it is useful to you, say hello on the links below.\n\n"
"<!-- Personalise this freely: add your real name, what you do, where you're based, why you built this. -->"
)
ABOUT_BN = (
"## কিউরেটর সম্পর্কে\n\n"
"আমি **theuglyhaxor**। এই গ্রন্থাগারটি গড়ে উঠেছে আমার দুটি দীর্ঘদিনের নেশা থেকে — একদিকে মৌলবাদী রাজনীতি ও ইতিহাস, অন্যদিকে নিরাপত্তা গবেষণা ও হ্যাকিং — আর এই সরল বিশ্বাস থেকে যে ভালো বই সহজলভ্য ও অবাধে পড়ার মতো হওয়া উচিত।\n\n"
"এখানে যা দেখছেন তা আমার নিজের পড়ার তাক: মার্ক্স ও মার্কসবাদী ধারা, ভারত ও বাংলাদেশের কমিউনিস্ট ও নকশাল আন্দোলন, জাতপাত ও দলিত সাহিত্য, কাশ্মীর ও প্যালেস্টাইন, বাংলা সাহিত্য এবং একটি কার্যকর সাইবার-নিরাপত্তা সংগ্রহ। আমি এটিকে গুছিয়েছি, প্রতিটি ফাইলকে প্রকৃত নাম দিয়েছি, বিষয় অনুযায়ী সাজিয়েছি, পাঠ-স্তর দিয়েছি এবং উপরের মানচিত্রগুলো এঁকেছি — যাতে নতুন পাঠক শত শত পিডিএফের ভিড়ে না হারিয়ে পথ খুঁজে পান।\n\n"
"এর কিছু যদি আপনার কাজে লাগে, নিচের লিঙ্কে যোগাযোগ করুন।\n\n"
"<!-- নিজের মতো করে সাজিয়ে নিন: আসল নাম, পেশা, অবস্থান যোগ করুন। -->"
)
SOCIAL = (
"## Connect — theuglyhaxor\n\n"
"[![X](https://img.shields.io/badge/X-%40theuglyhaxor-000000?logo=x&logoColor=white)](https://x.com/theuglyhaxor) "
"[![Facebook](https://img.shields.io/badge/Facebook-theuglyhaxor-1877F2?logo=facebook&logoColor=white)](https://facebook.com/theuglyhaxor) "
"[![LinkedIn](https://img.shields.io/badge/LinkedIn-theuglyhaxor-0A66C2?logo=linkedin&logoColor=white)](https://linkedin.com/in/theuglyhaxor) "
"[![YouTube](https://img.shields.io/badge/YouTube-theuglyhaxor-FF0000?logo=youtube&logoColor=white)](https://youtube.com/@theuglyhaxor)\n\n"
"| Platform | Handle |\n|----------|--------|\n"
"| X (Twitter) | [@theuglyhaxor](https://x.com/theuglyhaxor) |\n"
"| Facebook | [theuglyhaxor](https://facebook.com/theuglyhaxor) |\n"
"| LinkedIn | [theuglyhaxor](https://linkedin.com/in/theuglyhaxor) |\n"
"| YouTube | [@theuglyhaxor](https://youtube.com/@theuglyhaxor) |\n\n"
"*If you find this library useful, a follow is appreciated. Books are shared for education and study.*"
)

open(r"d:/READING/README.md","w",encoding="utf-8").write(build_en())
open(r"d:/READING/README.bn.md","w",encoding="utf-8").write(build_bn())
print("English + Bengali READMEs written.  books:",total,
      " levels:",dict(levels))

import json,sys,os
sys.path.insert(0,os.path.dirname(__file__))
from biz import BIZ
from reps import REPS, ELEMENTS, LEVELS
import ads_src, ads_se, ads_classic, ads_email, ads_more
from ads_src import ITEMS, SRC, EVL
import beliefs_a, beliefs_b, beliefs_c
from beliefs_a import CARDS
from beliefs_src import BSRC
for c in CARDS:
    for k in c["src"]: assert k in BSRC,k
ids=[r["id"] for r in REPS]; assert len(set(ids))==len(ids)
assert len(set(i["id"] for i in ITEMS))==len(ITEMS)
M={"gropen":"dm_gropen25","westermans":"dm_westermans","braun":"woodpecker","reeder":"woodpecker","harris":"woodpecker","kreuzberger":"woodpecker","wmf5":"wmf_tests"}
for r in REPS:
    if r.get("src"):
        k=M.get(r["src"],r["src"]); assert k in SRC,k; r["src"]=k
D=dict(biz=BIZ,elements={k:dict(channel=v[0],level=v[1],label=v[2],what=v[3],kind=v[4]) for k,v in ELEMENTS.items()},levels=LEVELS,reps=REPS,
       ads=ITEMS,adsrc={k:dict(name=v[0],url=v[1]) for k,v in SRC.items()},evl=EVL,beliefs=CARDS,bsrc={k:dict(name=v[0],url=v[1]) for k,v in BSRC.items()})
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json.dump(D,open(f"{root}/data/content.json","w"),ensure_ascii=False,indent=0)
open(f"{root}/data/content.js","w").write("window.CCW="+json.dumps(D,ensure_ascii=False)+";\n")
from collections import Counter
print("reps",len(REPS),dict(Counter(r["level"] for r in REPS)),dict(Counter(r["mode"] for r in REPS)))
print("els",dict(Counter(r["el"] for r in REPS)))
print("ads",len(ITEMS),dict(Counter(i["ev"] for i in ITEMS)))
print("beliefs",len(CARDS))
# ---- SOURCES.md ----
L=["# Sources — Copy & Confidence Workshop","","Every real ad, email and fact in the site links here. Evidence labels:",""]
L+=[f"- **{v}**" for v in EVL.values()]
L+=["","## Real Ads Lab items",""]
for i in ITEMS:
    s=SRC.get(i["src"]); L.append(f"- `{i['id']}` [{EVL[i['ev']].split(' (')[0]}] {i['title']} — " + (f"[{s[0]}]({s[1]})" if s else "") + (f" · live search: <{i['url']}>" if i.get('url') else ""))
L+=["","## Images (public domain / CC BY-SA)",""]
for i in ITEMS:
    if i.get("img"): L.append(f"- `{i['img']['src']}` — {i['img']['credit']}" + (f" ([source]({SRC[i['img']['page']][1]}))" if i['img'].get('page') in SRC else ""))
L+=["","## 'Steal like a pro' structures (quoted)",""]
for r in REPS:
    if r.get("mode")=="steal": L.append(f"- `{r['id']}` {r['quote']} — [{SRC[r['src']][0]}]({SRC[r['src']][1]})")
L+=["","## Belief Builder sources",""]+[f"- `{k}` [{v[0]}]({v[1]})" for k,v in BSRC.items()]
L+=["","## All source registry entries",""]+[f"- `{k}` [{v[0]}]({v[1]})" for k,v in SRC.items()]
L+=["","## Teaching content","","- All 24 writing-rep businesses are fictional; their figures (prices, review counts, rankings) are examples written for practice.",
"- Model answers are generated in the browser from those fictional facts by named formulas (js/formulas.js). They are not real ads and contain no real customer quotes; the testimonial formula uses a [placeholder] for a real review.",
"- 8 Ads Lab items (`t-01`…`t-08`) are teaching examples, labelled as such.",
"- Meta Ad Library: nothing is scraped or copied (Meta's terms). Live tasks only link to a public search.",""]
open(f"{root}/SOURCES.md","w").write("\n".join(L))
print("SOURCES.md lines",len(L))

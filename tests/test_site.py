"""End-to-end tests for the Copy & Confidence Workshop.
Usage: python3 tests/test_site.py <base_url> [label] [--nolinks] [--shots]
Headless Chrome (Playwright, /usr/bin/google-chrome) at 1366x768 and 1440x900, then a source-link check."""
import sys, json, os, time, ssl, urllib.request, concurrent.futures, re
from playwright.sync_api import sync_playwright
BASE=sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:18766/"
LABEL=sys.argv[2] if len(sys.argv)>2 and not sys.argv[2].startswith("--") else "local"
NOLINKS="--nolinks" in sys.argv; SHOTS="--shots" in sys.argv
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results=[]
def check(name, ok, detail=""):
    results.append({"test":name,"pass":bool(ok),"detail":str(detail)[:300]}); print(("PASS " if ok else "FAIL ")+name+(" — "+str(detail)[:220] if (detail and not ok) else ""),flush=True)
def safe(name, fn):
    try: fn()
    except Exception as e: check(name+" (exception)", False, repr(e)[:260])
def go(pg,h,sel,timeout=6000):
    pg.evaluate(f"location.hash={json.dumps(h)}"); pg.wait_for_selector(sel,timeout=timeout,state="attached")
def settle(pg):  # wait until the router has rendered the current hash
    pg.wait_for_function("(()=>{const m=location.hash.match(/^#\\/(w|a|b)\\/([^?]+)/);if(!m)return true;const a={w:'data-rep',a:'data-ad',b:'data-belief'}[m[1]];return !!document.querySelector(`[${a}='${m[2]}']`)})()")
def S(pg): return pg.evaluate("JSON.parse(JSON.stringify(CCWAPP.S))")
def fresh(pg):
    pg.goto(BASE+"#/"); pg.wait_for_selector("#homeView"); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_selector("#homeView")
def rect(pg,sel): return pg.evaluate(f"(()=>{{const e=document.querySelector({json.dumps(sel)});if(!e)return null;const r=e.getBoundingClientRect();return {{l:r.left,r:r.right,t:r.top,b:r.bottom,w:innerWidth,h:innerHeight,vis:r.width>0&&r.height>0}}}})()")
def next_corner(pg,tag,where,left_sel=None):
    n=rect(pg,"#btnNext")
    ok=n and n["vis"] and n["w"]-n["r"]<=30 and n["h"]-n["b"]<=24
    check(f"[{tag}] {where}: Next button is in the bottom-right corner", ok, n)
    if left_sel:
        a=rect(pg,left_sel); gap=(n["l"]-a["r"]) if (a and n) else None
        check(f"[{tag}] {where}: {left_sel} sits right next to Next (gap ≤ 16px, same row)", a and n and 0<=gap<=16 and abs(a["t"]-n["t"])<6, (a,n,gap))
def noscroll(pg,tag,where):
    sw=pg.evaluate("document.documentElement.scrollWidth-innerWidth"); check(f"[{tag}] no horizontal scroll: {where}", sw<=0, sw)
def fill(pg,sel,text):
    pg.fill(sel,text)
def model0(pg,el,biz):  # first model answer for an element+business (used as a strong draft)
    return pg.evaluate(f"(()=>{{const b=window.CCW.biz.find(x=>x.id==={json.dumps(biz)});return CCWAPP.gen({json.dumps(el)},b,b.lang)[0].t}})()")
def run_viewport(p,w,h,shots=False):
    tag=f"{w}x{h}"
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",headless=True)
    ctx=b.new_context(viewport={"width":w,"height":h},accept_downloads=True)
    pg=ctx.new_page(); errs=[]
    pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("pageerror",lambda e: errs.append("pageerror: "+str(e)))
    pg.on("dialog",lambda d: d.accept())
    fresh(pg)
    D=pg.evaluate("({reps:CCW.reps.map(r=>({id:r.id,mode:r.mode,el:r.el,level:r.level,biz:r.biz,lang:r.lang})),ads:CCW.ads.map(a=>({id:a.id,ev:a.ev,kind:a.kind,answer:a.answer,img:a.img?a.img.src:null,url:a.url||null,parts:a.parts.length})),bel:CCW.beliefs.map(b=>({id:b.id,script:!!b.script,src:b.src.length})),key:CCWAPP.KEY})")
    reps,ads,bel=D["reps"],D["ads"],D["bel"]
    real=[a for a in ads if a["ev"] not in ("teaching","live_adlib")]
    check(f"[{tag}] content counts: ≥150 reps, ≥60 lab items, 25–30 belief cards", len(reps)>=150 and len(ads)>=60 and 25<=len(bel)<=30, (len(reps),len(ads),len(bel)))
    check(f"[{tag}] all 6 levels, 14 elements and 5 rep modes present", {r["level"] for r in reps}=={1,2,3,4,5,6} and len({r["el"] for r in reps})==14 and {r["mode"] for r in reps}=={"guided","fix","steal","formula","ten"})
    check(f"[{tag}] lab mix: real {len(real)}, live {sum(a['ev']=='live_adlib' for a in ads)}, teaching {sum(a['ev']=='teaching' for a in ads)} — every item has an evidence label", len(real)>=40 and all(a["ev"] for a in ads))
    check(f"[{tag}] localStorage key is ccw-progress-v1 (not the playground's)", D["key"]=="ccw-progress-v1", D["key"])
    pg.wait_for_function("document.fonts.status==='loaded'",timeout=15000)
    fok=pg.evaluate("document.fonts.check('19px \"Atkinson Hyperlegible\"')"); ff=pg.evaluate("getComputedStyle(document.body).fontFamily")
    used=pg.evaluate("Array.from(document.fonts).some(f=>f.family.includes('Atkinson')&&f.status==='loaded')")
    check(f"[{tag}] Atkinson Hyperlegible loaded and applied", fok and used and "Atkinson" in ff, (fok,used,ff))
    bg=pg.evaluate("getComputedStyle(document.body).backgroundColor"); check(f"[{tag}] white background", bg in ("rgb(255, 255, 255)","rgba(0, 0, 0, 0)"), bg)
    # home
    check(f"[{tag}] home shows the 3 parts, daily flow, streak and overall progress", all(pg.locator(s).count()==1 for s in ["#partWork","#partLab","#partBel","#flowCard","#homeStreak","#homeOverall"]))
    noscroll(pg,tag,"home"); next_corner(pg,tag,"home")
    if shots: pg.wait_for_timeout(300); pg.screenshot(path=f"{ROOT}/shots/home.png")
    # ---- level lock + unlock by score ----
    go(pg,"#/w/"+[r for r in reps if r["level"]==2][0]["id"],"#lockCard")
    check(f"[{tag}] level 2 starts locked", pg.locator("#lockCard").count()==1)
    l1=[r for r in reps if r["level"]==1 and r["mode"]=="guided" and r["el"]=="headline"][:5]
    for r in l1:
        go(pg,"#/w/"+r["id"],f"[data-rep='{r['id']}'] #draftText"); fill(pg,"#draftText",model0(pg,"headline",r["biz"])); pg.click("#btnCheck"); pg.wait_for_selector("#checkerDraft")
    st=S(pg); sc=[st["reps"][r["id"]]["best"] for r in l1]
    check(f"[{tag}] 5 strong level-1 headlines score ≥70", all(x>=70 for x in sc), sc)
    check(f"[{tag}] level 2 unlocks after 5 reps ≥70", pg.evaluate("CCWAPP.unlocked(2)") and not pg.evaluate("CCWAPP.unlocked(3)"))
    go(pg,"#/workshop","#lvl-3 [data-ovr='3']"); pg.click("#ovr-3"); pg.wait_for_selector("#lvl-3:not(.locked)")
    check(f"[{tag}] manual override unlocks level 3", pg.evaluate("CCWAPP.unlocked(3)") and S(pg)["unlock"].get("3")==True)
    noscroll(pg,tag,"workshop")
    # ---- full rep flow with keyboard: draft → check → rewrite before/after → reveal → next ----
    r=[x for x in reps if x["level"]==1 and x["mode"]=="guided"][6]
    go(pg,"#/w/"+r["id"],f"[data-rep='{r['id']}'] #draftText")
    check(f"[{tag}] rep shows brief + 5 guided questions", pg.locator("#brief table.facts tr").count()>=5 and pg.locator("[data-g]").count()==5)
    for k,v in [("who","Solnabor"),("benefit","kontroll inom en vecka"),("proof","212 omdömen"),("offer","695 kr"),("action","boka")]: pg.fill(f"#g-{k}",v)
    fill(pg,"#draftText","Välkommen till oss, vi brinner för kvalitet!!")
    pg.focus("#draftText"); pg.keyboard.press("Control+Enter"); pg.wait_for_selector("#checkerDraft")
    s1=S(pg)["reps"][r["id"]]["ds"]
    check(f"[{tag}] Ctrl+Enter checks the draft; weak draft scores low with prioritised fixes", s1<60 and pg.locator("#checkerDraft .ckfix li").count()>=3, s1)
    gl=pg.locator("#checkerDraft [data-ck='guide']").count(); check(f"[{tag}] checker includes 'uses your guided answers' rule", gl==1)
    next_corner(pg,tag,"writing rep (after check)","#btnReveal")
    if shots: pg.locator("#checkerDraft").scroll_into_view_if_needed(); pg.wait_for_timeout(200); pg.screenshot(path=f"{ROOT}/shots/writing-rep-checker.png")
    fill(pg,"#rewriteText",model0(pg,r["el"],r["biz"])+" Boka på nätet på 2 minuter.")
    pg.evaluate("document.activeElement.blur()"); pg.keyboard.press("Enter"); pg.wait_for_selector("#baBox")
    st=S(pg)["reps"][r["id"]]
    check(f"[{tag}] Enter checks the rewrite; before/after side by side with higher score", st["rs"]>st["ds"] and pg.locator("#baBox .bacol").count()==2, (st["ds"],st["rs"]))
    pg.keyboard.press("Enter"); pg.wait_for_selector("#models .model")
    nm=pg.locator("#models .model[data-model]").count(); whys=pg.locator("#models .model .why").count()
    check(f"[{tag}] Enter reveals 3–5 model answers, each with a 'why it works'", 3<=nm<=5 and whys==nm, nm)
    names=pg.locator("#models .model strong").all_inner_texts(); check(f"[{tag}] model answers use different formulas", len(set(names))==len(names), names)
    if shots: pg.locator("#models").scroll_into_view_if_needed(); pg.wait_for_timeout(200); pg.screenshot(path=f"{ROOT}/shots/model-answers.png")
    pg.click(".swm >> nth=0"); check(f"[{tag}] ★ Save on a model adds it to the swipe file", len(S(pg)["swipe"])==1)
    before=pg.evaluate("location.hash"); pg.keyboard.press("Enter"); pg.wait_for_function(f"location.hash!=={json.dumps(before)}"); settle(pg)
    check(f"[{tag}] Enter after reveal goes to the next rep", pg.evaluate("location.hash").startswith("#/w/"))
    pg.keyboard.press("ArrowLeft"); pg.wait_for_function(f"location.hash==={json.dumps(before)}"); settle(pg); check(f"[{tag}] ← goes back", True)
    d0=S(pg)["reps"][r["id"]].get("done"); pg.keyboard.press("m"); pg.wait_for_timeout(100); d1=S(pg)["reps"][r["id"]].get("done"); check(f"[{tag}] M toggles done", d0!=d1, (d0,d1,pg.evaluate("location.hash"),pg.evaluate("document.activeElement.tagName"))); pg.keyboard.press("m")
    # keys c / r on another rep
    r2=[x for x in reps if x["level"]==1 and x["mode"]=="guided"][8]
    go(pg,"#/w/"+r2["id"],"#draftText"); fill(pg,"#draftText","Test rubrik 495 kr"); pg.evaluate("document.activeElement.blur()")
    pg.keyboard.press("c"); pg.wait_for_selector("#checkerDraft"); pg.keyboard.press("r"); pg.wait_for_selector("#models")
    check(f"[{tag}] C checks and R reveals", True)
    # formula + ten + fix + steal
    for mode in ["formula","ten","fix","steal"]:
        x=[q for q in reps if q["mode"]==mode][0]
        go(pg,"#/w/"+x["id"],f"[data-rep='{x['id']}']")
        if mode in ("formula","ten"):
            for i in range(3): pg.fill(f"#f-{i}",model0(pg,x["el"],x["biz"]))
            pg.click("#btnCheck"); pg.wait_for_selector("#ms-0 .schip")
            if mode=="ten": pg.click("#ts-1"); pg.wait_for_selector("#ts-1.on")
            pg.click("#btnReveal"); pg.wait_for_selector("#models .model")
            ok=S(pg)["reps"][x["id"]].get("fa") is not None and (mode!="ten" or S(pg)["reps"][x["id"]].get("star")==1)
        else:
            fill(pg,"#draftText",model0(pg,x["el"],x["biz"])); pg.click("#btnCheck"); pg.wait_for_selector("#checkerDraft"); pg.click("#btnReveal")
            pg.wait_for_selector("#expertFix" if mode=="fix" else "#stealModel"); ok=True
            if mode=="steal": ok=pg.locator("#stealQuote").count()==1 and pg.locator(".steal .srclink").count()==1
        check(f"[{tag}] mode '{mode}' works (write → check → reveal)", ok)
    # L6 timer
    x=[q for q in reps if q["level"]==6][0]; pg.evaluate("CCWAPP.S.unlock={2:true,3:true,4:true,5:true,6:true};CCWAPP.save()")
    go(pg,"#/w/"+x["id"],"#btnTimer"); pg.keyboard.press("t"); pg.wait_for_timeout(1300)
    tt=pg.inner_text("#btnTimer"); check(f"[{tag}] T starts the level-6 timer", "9:5" in tt or "9:4" in tt, tt); pg.keyboard.press("t")
    return b,ctx,pg,errs,reps,ads,bel,tag
def run_rest(b,ctx,pg,errs,reps,ads,bel,tag,shots):
    # own brief
    go(pg,"#/own","#ownForm"); pg.select_option("#ownLang","sv"); pg.select_option("#ownType","dentist"); pg.click("#btnOwnExample")
    pg.fill("#own-name","Testklinik Odenplan"); pg.select_option("#ownEl","headline"); pg.click("#btnNext"); pg.wait_for_selector("[data-rep='own'] #draftText")
    fill(pg,"#draftText","Odenplansbor: tandkontroll för 695 kr"); pg.click("#btnCheck"); pg.wait_for_selector("#checkerDraft"); pg.click("#btnReveal"); pg.wait_for_selector("#models .model")
    txt=" ".join(pg.locator("#models .model .mt").all_inner_texts())
    own_dbg=(pg.inner_text("#repTitle"),pg.input_value("#g-who"),pg.evaluate("CCWAPP.S.own.biz.city"),txt[:200])
    check(f"[{tag}] own-brief mode: guided steps + checker + template models built from MY fields", pg.locator("[data-g]").count()==5 and "Testklinik Odenplan" in pg.inner_text("#repTitle") and pg.input_value("#g-who")=="" and (pg.evaluate("CCWAPP.S.own.biz.city") in txt) and pg.locator("#models .model[data-model]").count()>=3, own_dbg)
    # every rep renders, checks and reveals
    pg.evaluate("CCWAPP.S.unlock={2:true,3:true,4:true,5:true,6:true};CCWAPP.save()")
    bad=[]
    for r in reps:
        try:
            go(pg,"#/w/"+r["id"],f"[data-rep='{r['id']}']")
            assert pg.locator("#brief table.facts tr").count()>=3 and pg.inner_text("#repTitle").strip()
            if r["mode"] in ("formula","ten"):
                assert pg.locator(".mtext").count()==10; pg.fill("#f-0",model0(pg,r["el"],r["biz"])); pg.click("#btnCheck"); pg.wait_for_selector("#ms-0 .schip",timeout=4000)
            else:
                pg.fill("#draftText",model0(pg,r["el"],r["biz"])); pg.click("#btnCheck"); pg.wait_for_selector("#checkerDraft .ckscore",timeout=4000)
            pg.click("#btnReveal"); pg.wait_for_selector("#models",timeout=4000)
            n=pg.locator("#models .model[data-model]").count(); assert 3<=n<=5, f"{n} models"
            assert "undefined" not in pg.inner_text("#main")
        except Exception as e: bad.append((r["id"],repr(e)[:120]))
    check(f"[{tag}] every one of {len(reps)} reps renders, checks and reveals 3–5 models", not bad, bad[:5])
    # Ads Lab: every item
    bad=[];pos=[]
    for i,a in enumerate(ads):
        try:
            go(pg,"#/a/"+a["id"],f"[data-ad='{a['id']}']")
            assert pg.locator("#adEv").inner_text().strip()
            if a["img"]: pg.wait_for_function("(()=>{const i=document.querySelector('figure.realad img');return i&&i.complete&&i.naturalWidth>0})()",timeout=8000)
            if a["kind"]=="live": assert "facebook.com/ads/library" in pg.get_attribute("#liveLink","href")
            assert "ghost" in pg.get_attribute("#btnNext","class")
            key="1" if (a["answer"]=="good" or (a["answer"] is None and i%2==0)) else "2"
            if i%3==0 and a["answer"]: key="2" if key=="1" else "1"  # deliberately miss some
            pg.keyboard.press(key); pg.wait_for_selector("#breakdownBox",timeout=4000)
            assert "ghost" not in pg.get_attribute("#btnNext","class"), "Next not primary after answering"
            if a["kind"]!="live": assert pg.locator("#breakdown tr[data-part]").count()==a["parts"] and a["parts"]>=4
            n=rect(pg,"#btnNext"); bb=rect(pg,"#btnBad"); pos.append(n["w"]-n["r"]<=30 and n["h"]-n["b"]<=24 and 0<=n["l"]-bb["r"]<=16)
            st=S(pg)["lab"][a["id"]]; assert st["pick"]==("good" if key=="1" else "bad")
        except Exception as e: bad.append((a["id"],repr(e)[:140]))
    check(f"[{tag}] every one of {len(ads)} lab items renders; 1/2 answers; breakdown shows; Next turns primary", not bad, bad[:5])
    check(f"[{tag}] Ads Lab: Next sits bottom-right right after Good/Bad on every item", all(pos) and len(pos)==len(ads), pos.count(False))
    a0=[a for a in ads if a["kind"]!="live" and a["answer"]][0]
    go(pg,"#/a/"+a0["id"]+"?again","#btnGood"); next_corner(pg,tag,"Ads Lab before answering","#btnBad")
    pg.keyboard.press("1" if a0["answer"]=="good" else "2"); pg.wait_for_selector("#breakdown"); next_corner(pg,tag,"Ads Lab after answering","#btnBad")
    if shots: pg.locator("#breakdownBox").scroll_into_view_if_needed(); pg.wait_for_timeout(200); pg.screenshot(path=f"{ROOT}/shots/ads-lab-breakdown.png")
    pg.keyboard.press("b"); check(f"[{tag}] B saves a lab item to the swipe file", ("ad:"+a0["id"]) in S(pg)["swipe"])
    hs=pg.evaluate("location.hash"); pg.keyboard.press("ArrowRight"); pg.wait_for_function(f"location.hash!=={json.dumps(hs)}"); settle(pg); check(f"[{tag}] → goes to the next lab item", True)
    noscroll(pg,tag,"Ads Lab item")
    # SRS
    st=S(pg); miss=[k for k in st["srs"] if k.startswith("a:")]
    check(f"[{tag}] missed lab items are scheduled for review tomorrow", len(miss)>0 and all(st["srs"][k]["step"]==0 for k in miss), len(miss))
    pg.evaluate("CCWAPP.setDayOffset(1)"); go(pg,"#/review","#reviewView")
    check(f"[{tag}] next day: missed items are due in Review", pg.locator("#dueList li").count()>=len(miss), pg.locator("#dueList li").count())
    pg.evaluate("CCWAPP.setDayOffset(0)")
    # beliefs: every card, ratings, chart, visual
    bad=[]
    for i,c in enumerate(bel):
        try:
            go(pg,"#/b/"+c["id"],f"[data-belief='{c['id']}']")
            assert pg.locator("svg#beliefVisual *").count()>=3
            assert pg.locator("#newBelief").count()==1 and pg.locator(".steps li").count()>=3 and pg.locator("#actDone").count()==1
            if c["script"]: assert pg.locator("#beliefScript li").count()>=2
            if c["src"]: assert pg.locator("#beliefSources a").count()==c["src"]
            pg.keyboard.press("8"); pg.wait_for_function("document.querySelector('#rateBefore').textContent==='8'")
            pg.keyboard.press("0" if i%2 else "4"); pg.wait_for_selector("#beliefChart circle")
            rr=S(pg)["beliefs"][c["id"]]["ratings"]; assert rr[-1]["before"]==8 and rr[-1]["after"]==(10 if i%2 else 4)
            pg.keyboard.press("m"); assert S(pg)["beliefs"][c["id"]]["done"]
        except Exception as e: bad.append((c["id"],repr(e)[:140]))
    check(f"[{tag}] every one of {len(bel)} belief cards renders (visual, steps, action, script, sources); before/after ratings save; chart draws; M marks done", not bad, bad[:5])
    c=bel[0]; go(pg,"#/b/"+c["id"],"#beliefVisual"); pg.click("#rate-6"); pg.click("#rate-3"); pg.wait_for_selector("#ratingTable")
    rr=S(pg)["beliefs"][c["id"]]["ratings"]; check(f"[{tag}] same belief can be done again the same day (unlimited); chart has 2 sessions", len(rr)==2 and pg.locator("#beliefChart circle").count()==4, len(rr))
    next_corner(pg,tag,"belief card","#rate-10")
    if shots: pg.wait_for_timeout(200); pg.locator("#beliefVisual").scroll_into_view_if_needed(); pg.screenshot(path=f"{ROOT}/shots/belief-card.png")
    noscroll(pg,tag,"belief card")
    tc=pg.evaluate("(CCWAPP.S.daily[CCWAPP.today()]||[]).length"); check(f"[{tag}] nothing is capped: today's count ({tc}) can exceed the daily target", tc>pg.evaluate("CCWAPP.S.goal"), tc)
    check(f"[{tag}] streak counts today once the target is hit", pg.evaluate("document.querySelector('#topStreak').textContent")=="1")
    go(pg,"#/beliefs","#beliefsView"); check(f"[{tag}] belief list shows all cards and done marks", pg.locator(".bcard").count()==len(bel) and pg.locator(".bcard.done").count()==len(bel))
    # copy bank
    go(pg,"#/bank","#bankView"); n=int(pg.inner_text("#bankCount"))
    check(f"[{tag}] copy bank saved every checked piece with a score; chart drawn", n>=len(reps) and pg.locator("#bankChart circle").count()>0, n)
    pg.select_option("#bankEl","subject"); pg.wait_for_selector("#bankView"); m=pg.locator(".bankitem").count()
    check(f"[{tag}] copy bank filter works", 0<m<n, (m,n))
    for bid,ext in [("#btnBankJSON",".json"),("#btnBankCSV",".csv"),("#btnBankMD",".md")]:
        with pg.expect_download() as dl: pg.click(bid)
        check(f"[{tag}] copy bank export {ext}", dl.value.suggested_filename.endswith(ext))
    check(f"[{tag}] swipe file lists saved items", pg.locator("#swipeList .swipecard").count()>=2)
    # dashboard, checker, review
    go(pg,"#/dashboard","#dashView"); check(f"[{tag}] dashboard: calendar, element table, levels, lab accuracy, beliefs", all(pg.locator(s).count()==1 for s in ["#calendar","#dashEl","#dashLv","#dashLab","#dashBel"]))
    noscroll(pg,tag,"dashboard"); next_corner(pg,tag,"dashboard")
    go(pg,"#/checker","#freeText"); pg.fill("#freeText","Trött på dina rynkor? Botox på 7 dagar!!!"); pg.evaluate("document.activeElement.blur()"); pg.keyboard.press("c"); pg.wait_for_selector("#checkerFree")
    sc=int(pg.inner_text("#checkerFree .ckscore")); check(f"[{tag}] free checker flags a policy-breaking clinic ad (score capped ≤ 40)", sc<=40 and pg.locator("#checkerFree [data-ck='policy']").count()==1, sc)
    sc=pg.evaluate("[CCWAPP.checkCopy('Solnabor: tandkontroll för 695 kr','headline','sv',{}).score, CCWAPP.checkCopy('Välkommen till oss – vi brinner för kvalitet!','headline','sv',{}).score, CCWAPP.checkCopy('GRATIS!!! Erbjudande','subject','sv',{}).score, CCWAPP.checkCopy('Vill du att jag skickar rapporten?','ask','sv',{}).score, CCWAPP.checkCopy('Hi Priya, just following up on my last email.','followup','en',{}).score]")
    check(f"[{tag}] checker scoring: strong > weak for headline, spam subject low, interest ask high, lazy follow-up low", sc[0]>=85 and sc[1]<=55 and sc[2]<=60 and sc[3]>=85 and sc[4]<=60, sc)
    # keyboard extras
    go(pg,"#/","#homeView"); pg.keyboard.press("?"); check(f"[{tag}] ? opens the shortcuts dialog", pg.is_visible("#helpDlg")); pg.keyboard.press("Escape"); check(f"[{tag}] Esc closes it", not pg.is_visible("#helpDlg"))
    pg.keyboard.press("f"); check(f"[{tag}] F enters focus mode", pg.evaluate("document.body.classList.contains('focus')")); pg.keyboard.press("Escape"); check(f"[{tag}] Esc exits focus mode", not pg.evaluate("document.body.classList.contains('focus')"))
    # daily flow
    pg.evaluate("CCWAPP.S.flow=null;CCWAPP.save()"); go(pg,"#/","#btnFlow"); pg.click("#btnFlow"); pg.wait_for_selector("#flowTag")
    fl=S(pg)["flow"]; kinds=[k[0] for k in fl["items"]]
    check(f"[{tag}] daily flow = 1 belief + 3 ads + 5 reps", kinds.count("b")==1 and kinds.count("a")==3 and kinds.count("w")==5 and pg.evaluate("location.hash").startswith("#/b/"), kinds)
    pg.click("#btnNext"); pg.wait_for_function("location.hash.startsWith('#/a/')"); settle(pg); check(f"[{tag}] flow Next moves to the first ad", "2/9" in pg.inner_text("#flowTag"))
    # export / reset / import / reload
    go(pg,"#/","#btnExport")
    with pg.expect_download() as dl: pg.click("#btnExport")
    path=f"/tmp/ccw-export-{tag}.json"; dl.value.save_as(path); before=S(pg)
    pg.click("#btnReset"); pg.wait_for_timeout(300); check(f"[{tag}] reset clears progress", S(pg)["bank"]==[] and S(pg)["reps"]=={})
    go(pg,"#/","#fileImport"); pg.set_input_files("#fileImport",path); pg.wait_for_function("CCWAPP.S.bank.length>0",timeout=5000)
    check(f"[{tag}] import restores progress", len(S(pg)["bank"])==len(before["bank"]) and S(pg)["beliefs"]==before["beliefs"])
    pg.reload(); pg.wait_for_selector("#homeView"); after=S(pg)
    check(f"[{tag}] progress survives a reload", len(after["bank"])==len(before["bank"]) and after["lab"]==before["lab"] and after["beliefs"]==before["beliefs"])
    check(f"[{tag}] no console errors", not errs, errs[:5])
    b.close()
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
BOTBLOCK=("facebook.com","digitaltmuseum","linkedin.com","acquisition.com","ted.com","elcompanies","doi.org","journals.sagepub","psycnet","apa.org","bloomberg.com","loc.gov","wikimedia.org","wikipedia.org")
def all_links():
    D=json.load(open(f"{ROOT}/data/content.json"))
    U=set(v["url"] for v in D["adsrc"].values())|set(v["url"] for v in D["bsrc"].values())|set(a["url"] for a in D["ads"] if a.get("url"))
    U|=set(re.findall(r"\((https?://(?:[^()\s]|\([^()\s]*\))+)\)",open(f"{ROOT}/SOURCES.md").read()))|set(re.findall(r"<(https?://[^>\s]+)>",open(f"{ROOT}/SOURCES.md").read()))
    return sorted(U)
def fetch(u):
    ctx=ssl.create_default_context()
    for method in ("HEAD","GET"):
        try:
            rq=urllib.request.Request(u,method=method,headers={"User-Agent":UA,"Accept":"text/html,application/pdf,*/*","Accept-Language":"sv,en;q=0.8"})
            with urllib.request.urlopen(rq,timeout=25,context=ctx) as r: return r.status
        except urllib.error.HTTPError as e:
            if method=="GET" or e.code not in (403,405,404,400,429,501): return e.code
        except Exception as e:
            if method=="GET": return repr(e)[:80]
    return "?"
def link_check(p):
    U=all_links(); out={}
    with concurrent.futures.ThreadPoolExecutor(12) as ex:
        for u,s in zip(U,ex.map(fetch,U)): out[u]=s
    # anything not 2xx/3xx: retry in real Chrome (some sites block scripted clients)
    retry=[u for u,s in out.items() if not (isinstance(s,int) and s<400)]
    if retry:
        b=p.chromium.launch(executable_path="/usr/bin/google-chrome",headless=True); pg=b.new_page(user_agent=UA)
        for u in retry:
            try:
                r=pg.goto(u,timeout=30000,wait_until="domcontentloaded"); out[u]=f"chrome {r.status if r else '?'}"
            except Exception as e: out[u]=f"chrome {repr(e)[:60]}"
        b.close()
    def ok(u,s):
        m=re.search(r"(\d{3})",str(s)); code=int(m.group(1)) if m else None
        if code and code<400: return True
        return any(h in u for h in BOTBLOCK) and (code in (403,429,None) or "Timeout" in str(s) or "ERR_" in str(s))
    bad={u:s for u,s in out.items() if not ok(u,s)}
    allowed={u:s for u,s in out.items() if ok(u,s) and not re.search(r"\b[23]\d\d\b",str(s))}
    json.dump(out,open(f"{ROOT}/tests/link-status-{LABEL}.json","w"),indent=1)
    check(f"[links] all {len(U)} source links resolve ({len(allowed)} bot-blocked by known hosts, allowed)", not bad, bad)
if __name__=="__main__":
    t0=time.time()
    with sync_playwright() as p:
        for i,(w,h) in enumerate([(1366,768),(1440,900)]):
            sh=SHOTS and i==0
            try:
                st=run_viewport(p,w,h,sh); run_rest(*st,sh)
            except Exception as e:
                import traceback; tb=traceback.format_exc().splitlines(); check(f"[{w}x{h}] run (exception)",False,repr(e)[:200]+" @ "+" | ".join(l.strip() for l in tb if "test_site.py" in l)[-300:])
        if not NOLINKS: safe("[links] link check", lambda: link_check(p))
    n=len(results); passed=sum(r["pass"] for r in results)
    json.dump({"label":LABEL,"base":BASE,"passed":passed,"total":n,"seconds":round(time.time()-t0),"results":results},open(f"{ROOT}/tests/results-{LABEL}.json","w"),indent=1)
    print(f"\n{passed}/{n} passed in {round(time.time()-t0)}s"); sys.exit(0 if passed==n else 1)

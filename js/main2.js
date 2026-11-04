/* review, dashboard, free checker, keyboard, router, test hooks */
function viewReview(){setNav("navReview");const due=dueKeys(),t0=today();const up=Object.keys(S.srs).filter(k=>srsValid(k)&&S.srs[k].due>t0).sort((a,b)=>S.srs[a].due<S.srs[b].due?-1:1);
 const miss=ADS.filter(a=>S.lab[a.id]&&S.lab[a.id].correct===false),low=REPS.filter(r=>repBest(r.id)!=null&&repBest(r.id)<70);
 let h=`<div class="wrap" id="reviewView"><h1>Review</h1><p class="sub">Spaced repetition: Ads Lab items you get wrong and reps that score under 70 come back after 1 day, then 3, 7, 14 and 30 days each time you get them right on their due day.</p>
 <div class="card"><h2 style="margin-top:0">Due today <span class="pill" id="dueCount">${due.length}</span></h2>${due.length?`<ol class="reviewlist" id="dueList">${due.map(k=>`<li><a href="${keyHref(k)}?due">${esc(keyTitle(k))}</a> <span class="sub">step ${S.srs[k].step+1}/${INTERVALS.length}</span></li>`).join("")}</ol>`:`<p>Nothing due today.${up.length?` Next review: <strong>${S.srs[up[0]].due}</strong>.`:""}</p>`}</div>
 <h2>Ads Lab misses (${miss.length})</h2>${miss.length?`<ol class="reviewlist">${miss.map(a=>`<li><a href="#/a/${a.id}?again">${esc(a.title)}</a></li>`).join("")}</ol>`:`<p class="sub">None.</p>`}
 <h2>Reps under 70 (${low.length})</h2>${low.length?`<ol class="reviewlist">${low.map(r=>`<li><a href="#/w/${r.id}">${esc(repTitle(r))}</a> ${scoreChip(repBest(r.id))}</li>`).join("")}</ol>`:`<p class="sub">None.</p>`}
 ${up.length?`<h2>Coming up</h2><table class="stats wide" id="upcoming"><tr><th>Due</th><th>Item</th><th>Step</th></tr>${up.slice(0,30).map(k=>`<tr><td>${S.srs[k].due}</td><td><a href="${keyHref(k)}">${esc(keyTitle(k))}</a></td><td>${S.srs[k].step+1}/${INTERVALS.length}</td></tr>`).join("")}</table>`:""}</div>`;
 $("#main").innerHTML=h;LABUI.reviewing=true;setBar([],due.length?{label:`Review ${due.length} due →`,primary:true,on:()=>go(keyHref(due[0])+"?due")}:{label:"Home →",on:()=>go("#/")});}
function viewDash(){setNav("navDash");const rows=Object.keys(D.elements).map(el=>{const L=REPS.filter(r=>r.el===el),sc=L.map(r=>repBest(r.id)).filter(x=>x!=null);return {el,n:L.length,d:L.filter(r=>repDone(r.id)).length,avg:sc.length?Math.round(sc.reduce((a,b)=>a+b,0)/sc.length):null};});
 const fails={};S.bank.slice(-200).forEach(e=>{const r=checkCopy(e.text,kindOf(e.el),e.lang,{});r.results.forEach(x=>{if(!x.ok){fails[x.label]=(fails[x.label]||0)+1;}});});const topF=Object.entries(fails).sort((a,b)=>b[1]-a[1]).slice(0,6);
 const days=[];for(let i=27;i>=0;i--){const ds=addDays(today(),-i);days.push([ds,(S.daily[ds]||[]).length]);}
 const bel=BEL.map(b=>{const r=(S.beliefs[b.id]||{}).ratings||[];return {b,n:r.length,first:r[0],last:r[r.length-1]};}).filter(x=>x.n);
 let h=`<div class="wrap" id="dashView"><h1>Dashboard</h1>
 <h2>Last 28 days</h2><div class="cal" id="calendar">${days.map(([ds,n])=>`<div class="day ${n>=S.goal?"met":n?"some":""}" title="${ds}: ${n}"><span>${ds.slice(8)}</span><b>${n||""}</b></div>`).join("")}</div><p class="sub">Green = hit your target (${S.goal}). Streak: 🔥 ${streak()}.</p>
 <h2>Writing: by element</h2><table class="stats wide" id="dashEl"><tr><th>Element</th><th>Done</th><th class="barcell">Average best score</th><th class="num">Avg</th></tr>${rows.map(x=>`<tr><td>${esc(elLabel(x.el))}</td><td>${x.d}/${x.n}</td><td class="barcell"><div class="bar"><div class="${x.avg!=null&&x.avg<70?"lowb":""}" style="width:${x.avg||0}%"></div></div></td><td class="num">${x.avg==null?"–":x.avg}</td></tr>`).join("")}</table>
 <h2>Writing: levels</h2><table class="stats wide" id="dashLv"><tr><th>Level</th><th>Done</th><th>Scored 70+</th><th>Status</th></tr>${D.levels.map(l=>`<tr><td>L${l.n} ${esc(l.title)}</td><td>${levelReps(l.n).filter(r=>repDone(r.id)).length}/${levelReps(l.n).length}</td><td>${levelGood(l.n)}</td><td>${earned(l.n)?"unlocked":S.unlock[l.n]?"unlocked (override)":"🔒 locked"}</td></tr>`).join("")}</table>
 <h2>What the checker flags most in your copy</h2>${topF.length?`<ol id="dashFails">${topF.map(([k,n])=>`<li>${esc(k)} <span class="sub">(${n}×)</span></li>`).join("")}</ol>`:`<p class="sub">Write and check a few reps first.</p>`}
 <h2>Real Ads Lab</h2><table class="stats wide" id="dashLab"><tr><th>Evidence</th><th class="num">Accuracy</th></tr>${Object.keys(D.evl).filter(k=>k!=="live_adlib").map(k=>`<tr><td>${esc(D.evl[k])}</td><td class="num">${pct(labAcc(x=>x.ev===k))}</td></tr>`).join("")}<tr><td><strong>All</strong></td><td class="num"><strong>${pct(labAcc())}</strong></td></tr></table>
 <h2>Beliefs: first → latest rating</h2>${bel.length?`<table class="stats wide" id="dashBel"><tr><th>Belief</th><th>Sessions</th><th class="num">First (before)</th><th class="num">Latest (after)</th></tr>${bel.map(x=>`<tr><td><a href="#/b/${x.b.id}">${esc(x.b.belief)}</a></td><td>${x.n}</td><td class="num">${x.first.before}</td><td class="num">${x.last.after}</td></tr>`).join("")}</table>`:`<p class="sub">Rate a belief card before and after to see it here.</p>`}</div>`;
 $("#main").innerHTML=h;setBar([],{label:"Start today's flow →",primary:true,on:flowStart});}
function viewChecker(){setNav("navCheck");const lang=S.freeLang||"sv",kind=S.freeKind||"fullad";
 let h=`<div class="wrap" id="checkerView"><h1>Copy checker</h1><p class="sub">Paste any ad, email or line you're about to send. Rule-based, in your browser — no AI, nothing leaves this page.</p>
 <div class="swipebar"><select id="freeKind">${Object.keys(D.elements).map(k=>`<option value="${k}" ${kind===k?"selected":""}>${esc(elLabel(k))}</option>`).join("")}</select><select id="freeLang"><option value="sv" ${lang==="sv"?"selected":""}>Svenska</option><option value="en" ${lang==="en"?"selected":""}>English</option></select></div>
 <textarea id="freeText" class="big" placeholder="Paste or write your copy… (Ctrl+Enter = check)">${esc(S.free||"")}</textarea><div id="freeResult"></div></div>`;
 $("#main").innerHTML=h;$("#freeText").oninput=e=>{S.free=e.target.value;save();};$("#freeKind").onchange=e=>{S.freeKind=e.target.value;save();};$("#freeLang").onchange=e=>{S.freeLang=e.target.value;save();};
 setBar([{id:"btnFreeSave",label:"Save to copy bank",cls:"ghost",key:"b",on:()=>{const t=$("#freeText").value;if(!t.trim())return;const r=checkCopy(t,kindOf($("#freeKind").value),$("#freeLang").value,{});S.bank.push({id:uid(),rep:"free",el:$("#freeKind").value,lang:$("#freeLang").value,mode:"free",biz:"Free checker",stage:"free",text:t,score:r.score,at:Date.now(),star:false});save();toast("Saved to copy bank");}},{id:"btnFreeCheck",label:"Check",key:"c",primary:true,on:freeCheck}],{label:"Workshop →",on:()=>go("#/workshop")});}
function freeCheck(){const t=$("#freeText").value,l=$("#freeLang").value;$("#freeResult").innerHTML=checkerHTML(checkCopy(t,kindOf($("#freeKind").value),l,{}),l,"checkerFree");}
/* keyboard */
function toggleHelp(force){const d=$("#helpDlg");const show=force!=null?force:d.hidden;d.hidden=!show;}
document.addEventListener("keydown",e=>{const t=e.target,typing=t.matches&&t.matches("textarea,input[type=text],input[type=search],input[type=number],select");
 if(typing){if(e.key==="Enter"&&(e.ctrlKey||e.metaKey)){e.preventDefault();t.blur();barPrimary();}else if(e.key==="Escape"){t.blur();}return;}
 if(e.ctrlKey||e.metaKey||e.altKey)return;
 if(e.key==="?"){e.preventDefault();toggleHelp();return;}
 if(e.key==="Escape"){if(!$("#helpDlg").hidden)return toggleHelp(false);document.body.classList.remove("focus");return;}
 if(e.key==="Enter"){if(t.tagName==="A"&&!t.closest("#actionbar"))return;e.preventDefault();barPrimary();return;}
 if(e.key==="ArrowRight"){if(BAR.next){e.preventDefault();BAR.next.on();}return;}
 if(e.key==="ArrowLeft"){if(BAR.opts.back){e.preventDefault();BAR.opts.back();}return;}
 const k=e.key.toLowerCase();
 if(k==="f"){document.body.classList.toggle("focus");return;}
 if(k==="b"&&BAR.opts.save){BAR.opts.save();return;}
 const b=BAR.btns.find(x=>x.key===k);if(b){e.preventDefault();b.on();}});
/* router */
function route(){const h=location.hash||"#/";const [path,q]=h.split("?");const p=path.replace(/^#\//,"").split("/");window.scrollTo(0,0);if(REPUI.timer&&!(p[0]==="w"&&p[1]===REPUI.id)){clearInterval(REPUI.timer);REPUI.timer=null;}
 if(p[0]!=="review"&&q!=="due")LABUI.reviewing=LABUI.reviewing&&p[0]==="a";
 if(p[0]==="workshop")viewWorkshop();else if(p[0]==="w"&&p[1])viewRep(p[1]);else if(p[0]==="own")viewOwn();else if(p[0]==="lab")viewLab();else if(p[0]==="a"&&p[1])viewAd(p[1],q);
 else if(p[0]==="beliefs")viewBeliefs();else if(p[0]==="b"&&p[1])viewBelief(p[1]);else if(p[0]==="bank")viewBank();else if(p[0]==="review")viewReview();else if(p[0]==="dashboard")viewDash();else if(p[0]==="checker")viewChecker();else viewHome();
 updateTop();$("#main").focus({preventScroll:true});}
window.addEventListener("hashchange",route);
window.addEventListener("storage",e=>{if(e.key===KEY){S=load();route();}});
window.CCWAPP={get S(){return S;},set S(v){S=v;},save,load,blank,checkCopy,gen,route,KEY,setDayOffset(n){dayOffset=n;},today,unlocked,levelGood,REPS,ADS,BEL,dueKeys,buildFlow};
document.addEventListener("DOMContentLoaded",()=>{$("#helpList").innerHTML=KBD.map(([k,v])=>`<li><span class="kbd">${k}</span> ${v}</li>`).join("");$("#helpClose").onclick=()=>toggleHelp(false);$("#btnHelp").onclick=()=>toggleHelp(true);$("#focusExit").onclick=()=>document.body.classList.remove("focus");route();});

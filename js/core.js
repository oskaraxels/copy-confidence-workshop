/* Copy & Confidence Workshop — core: data, state, dates, daily goal, SRS, helpers */
"use strict";
const D=window.CCW, KEY="ccw-progress-v1", INTERVALS=[1,3,7,14,30];
const REPS=D.reps, REP={}; REPS.forEach((r,i)=>{r._i=i;REP[r.id]=r;});
const BIZ={}; D.biz.forEach(b=>BIZ[b.id]=b);
const ADS=D.ads, AD={}; ADS.forEach((a,i)=>{a._i=i;AD[a.id]=a;});
const BEL=D.beliefs, BL={}; BEL.forEach((b,i)=>{b._i=i;BL[b.id]=b;});
let dayOffset=0;
function dstr(d){return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;}
function today(){const d=new Date();d.setDate(d.getDate()+dayOffset);return dstr(d);}
function addDays(ds,n){const [y,m,x]=ds.split("-").map(Number);const d=new Date(y,m-1,x);d.setDate(d.getDate()+n);return dstr(d);}
function blank(){return {v:1,app:"ccw",goal:9,daily:{},reps:{},bank:[],unlock:{},lab:{},srs:{},beliefs:{},swipe:{},own:null,flow:null,free:"",freeLang:"sv",freeKind:"fullad",lastRep:null,lastAd:null,timer:null};}
function migrate(s){const o=Object.assign(blank(),s);["daily","reps","unlock","lab","srs","beliefs","swipe"].forEach(k=>{if(!o[k]||typeof o[k]!=="object"||Array.isArray(o[k]))o[k]={};});if(!Array.isArray(o.bank))o.bank=[];if(!(o.goal>0))o.goal=9;return o;}
function load(){try{const s=JSON.parse(localStorage.getItem(KEY)||"null");if(s&&s.v===1&&s.app==="ccw")return migrate(s);}catch(e){}return blank();}
let S=load();
function save(){try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}}
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function toast(m){const t=$("#toast");t.textContent=m;t.classList.add("show");clearTimeout(toast._t);toast._t=setTimeout(()=>t.classList.remove("show"),1800);}
function cap(s){s=String(s||"");return s.charAt(0).toUpperCase()+s.slice(1);}
function lc(s){s=String(s||"");return s.charAt(0).toLowerCase()+s.slice(1);}
function nodot(s){return String(s||"").replace(/[.!\s]+$/,"");}
function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,6);}
function download(name,type,text){const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},100);}
/* daily goal (a target, never a cap) + streak */
function markDaily(key){const t=today();S.daily[t]=S.daily[t]||[];if(!S.daily[t].includes(key))S.daily[t].push(key);}
function todayCount(){return (S.daily[today()]||[]).length;}
function todayBy(p){return (S.daily[today()]||[]).filter(k=>k.startsWith(p+":")).length;}
function streak(){let n=0,d=today();if((S.daily[d]||[]).length<S.goal)d=addDays(d,-1);while((S.daily[d]||[]).length>=S.goal){n++;d=addDays(d,-1);}return n;}
/* spaced repetition: key = "a:<adId>" (missed lab item) or "w:<repId>" (rep scored < 70) */
function srsValid(k){const [p,id]=[k.slice(0,1),k.slice(2)];return p==="a"?!!AD[id]:p==="w"?!!REP[id]:false;}
function dueKeys(){const t=today();return Object.keys(S.srs).filter(k=>srsValid(k)&&S.srs[k].due<=t).sort((a,b)=>S.srs[a].due<S.srs[b].due?-1:1);}
function schedule(k,ok){const t=today(),cur=S.srs[k];
 if(ok===false){S.srs[k]={step:0,due:addDays(t,1),last:t};return;}
 if(ok===true&&cur&&cur.due<=t){const step=cur.step+1;if(step>=INTERVALS.length)delete S.srs[k];else S.srs[k]={step,due:addDays(t,INTERVALS[step]),last:t};}}
function keyHref(k){return k[0]==="a"?`#/a/${k.slice(2)}`:`#/w/${k.slice(2)}`;}
function keyTitle(k){const id=k.slice(2);if(k[0]==="a")return AD[id]?AD[id].title:id;const r=REP[id];return r?repTitle(r):id;}
/* reps: progress + level unlocks */
function rs(id){return S.reps[id]=S.reps[id]||{};}
function repBest(id){const r=S.reps[id];return r&&r.best!=null?r.best:null;}
function repDone(id){const r=S.reps[id];return !!(r&&r.done);}
function levelReps(n){return REPS.filter(r=>r.level===n);}
function levelGood(n){return levelReps(n).filter(r=>(repBest(r.id)||0)>=70).length;}
const UNLOCK_N=5, UNLOCK_SCORE=70;
function earned(n){return n<=1||levelGood(n-1)>=UNLOCK_N;}
function unlocked(n){return earned(n)||!!S.unlock[n];}
function elLabel(el){return (D.elements[el]||{}).label||el;}
function repTitle(r){const b=r.biz==="own"?((S.own||{}).biz||{}):(BIZ[r.biz]||{});const m={guided:"",fix:"Fix this weak line · ",steal:"Steal like a pro · ",formula:"Formula drill · ",ten:"10 versions · "}[r.mode]||"";return `${m}${elLabel(r.el)} — ${b.name||"Your brief"}`;}
function evClass(e){return "ev "+e;}
function evLabel(e){return D.evl[e]||e;}
function srcLink(key,label){const s=D.adsrc[key]||D.bsrc[key];if(!s)return "";return `<a class="srclink" href="${esc(s.url)}" target="_blank" rel="noopener">${esc(label||s.name)} ↗</a>`;}

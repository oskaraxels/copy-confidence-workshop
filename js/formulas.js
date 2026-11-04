/* Model-answer formulas. Every model answer is generated from the brief's own (fictional, example) facts with a named formula — the same code powers "Your own brief". Nothing here is a real ad or a real customer quote. */
const BFIELDS=["name","city","who","reader","service","outcome","friction","fact","proof","offer","price","risk","cta","visual","owner","kw","hookFact","obs","obs2","emailOffer","offerShort","myProof","ask"];
function fillBiz(b,sv){const o=Object.assign({},b);BFIELDS.forEach(k=>{if(!String(o[k]||"").trim())o[k]=`[${k}]`;});return o;}
const F={
 headline:[
  {n:"Reader + offer",p:"[Reader]: [offer]",w:"Calls out the exact reader, then says what they get (Hopkins: the headline picks the reader).",f:(b,sv)=>`${b.who}: ${b.offer}`},
  {n:"Question",p:"Want to [outcome]?",w:"A question the right reader answers 'yes' to in their head.",f:(b,sv)=>sv?`Vill du ${b.outcome}?`:`Want to ${b.outcome}?`},
  {n:"How to",p:"How to [outcome]",w:"Promises useful information — Caples' 'how to' headlines are long-proven.",f:(b,sv)=>sv?`Så kan du ${b.outcome}`:`How to ${b.outcome}`},
  {n:"Offer + place",p:"[Offer] in [city]",w:"Local + concrete: the reader knows it's near and what it is.",f:(b,sv)=>`${cap(b.offer)} ${sv?"i":"in"} ${b.city}`},
  {n:"Proof first",p:"[Proof] – [name]",w:"Leads with a checkable fact instead of a claim (Ogilvy: facts sell).",f:(b,sv)=>`${cap(b.proof)} – ${b.name}`},
  {n:"News",p:"New in [city]: [offer]",w:"'New' is one of Ogilvy's strongest headline words — only use it if it IS new.",f:(b,sv)=>sv?`Nytt i ${b.city}: ${b.offer}`:`New in ${b.city}: ${b.offer}`},
  {n:"Without the hassle",p:"[Service] without having to [friction]",w:"Removes the exact annoyance that stops the reader.",f:(b,sv)=>sv?`${cap(b.service)} utan att ${b.friction}`:`${cap(b.service)} without having to ${b.friction}`},
  {n:"Price-first",p:"[Service] in [city] – [price]",w:"A price up front filters in buyers and builds trust.",f:(b,sv)=>b.price&&!/^\[/.test(b.price)?`${cap(b.service)} ${sv?"i":"in"} ${b.city} – ${b.price}`:null},
  {n:"Reason why",p:"Why [readers] choose [name]",w:"Promises reasons — Hopkins' 'reason-why' copy.",f:(b,sv)=>sv?`Därför väljer ${lc(b.who)} ${b.name}`:`Why ${lc(b.who)} choose ${b.name}`},
  {n:"Risk reversal",p:"[Offer]. [Risk removed]",w:"Takes away the fear of being tricked (Hopkins: the free sample, money back).",f:(b,sv)=>`${cap(b.offer)}. ${b.risk}`},
  {n:"Command + offer",p:"[CTA] – [offer]",w:"Tells the reader exactly what to do and what they get.",f:(b,sv)=>`${nodot(b.cta)} – ${b.offer}`},
  {n:"Testimonial (real reviews only)",p:"“[real review]” – [proof]",w:"Social proof — but ONLY with a real review used with permission. Never invent one.",f:(b,sv)=>sv?`”[Ett riktigt omdöme om ${b.service}, med kundens lov]” – ${b.proof}`:`"[A real review about ${b.service}, with permission]" – ${b.proof}`},
 ],
 subject:[
  {n:"Name + fact",p:"[name], [fact about them]",w:"Their name + something specific about THEM. Looks like a normal email.",f:(b,sv)=>b.hookFact?`${b.owner}, ${b.hookFact}`:null},
  {n:"Their search term",p:"[keyword]",w:"Lowercase, the exact phrase their customers type — instantly relevant.",f:(b,sv)=>b.kw?lc(b.kw):null},
  {n:"Question about them",p:"question about [business]",w:"Plain and personal, like a colleague would write.",f:(b,sv)=>sv?`fråga om ${b.name}`:`question about ${b.name}`},
  {n:"Free thing for them",p:"[free thing] for [business]",w:"Says what's inside: a gift, made for them.",f:(b,sv)=>`${b.offerShort} ${sv?"för":"for"} ${b.name}`},
  {n:"Two-word topic",p:"[business] + [topic]",w:"Short subjects that look personal tend to get opened.",f:(b,sv)=>b.pitch==="meta"?(sv?`${b.name}s annonser`:`${b.name}'s ads`):(sv?`${b.name} i kartan`:`${b.name} on Google Maps`)},
  {n:"Curiosity (honest)",p:"noticed something about [business]",w:"Honest curiosity — the email must deliver what the subject hints at.",f:(b,sv)=>sv?`såg något om ${b.name}`:`noticed something about ${b.name}`},
  {n:"Service + place",p:"[service] [city]",w:"What their customers search for, lowercase.",f:(b,sv)=>lc(`${b.service} ${b.city}`)},
  {n:"Idea for them",p:"idea for [business]",w:"Promises value, not a pitch.",f:(b,sv)=>sv?`idé till ${b.name}`:`idea for ${b.name}`},
  {n:"Just the name",p:"[name]?",w:"The shortest personal subject there is.",f:(b,sv)=>`${b.owner}?`},
  {n:"The fact alone",p:"[fact]",w:"One specific fact they'll want to check.",f:(b,sv)=>b.hookFact||null},
 ],
 hook:[
  {n:"Reader question + fact",p:"[Reader situation]? [One fact]",w:"Picks the reader in line 1, then gives a reason to keep reading.",f:(b,sv)=>`${nodot(b.reader)}? ${b.fact}`},
  {n:"Reader + outcome",p:"[Readers]: you can now [outcome].",w:"Names the reader and the result they want.",f:(b,sv)=>sv?`${b.who}: nu kan du ${b.outcome}.`:`${b.who}: you can now ${b.outcome}.`},
  {n:"No hassle",p:"You don't have to [friction] to [outcome].",w:"Names the friction and removes it.",f:(b,sv)=>sv?`Du behöver inte ${b.friction} för att ${b.outcome}.`:`You don't have to ${b.friction} to ${b.outcome}.`},
  {n:"Proof first",p:"[Proof]. [Fact]",w:"A checkable number is more believable than an adjective.",f:(b,sv)=>`${cap(b.proof)}. ${b.fact}`},
  {n:"Offer first",p:"[Offer], [city]. [Risk removed]",w:"Leads with what they get — no warm-up.",f:(b,sv)=>`${cap(b.offer)}, ${b.city}. ${b.risk}`},
  {n:"Price-led",p:"[Price] – [service] in [city].",w:"A number in the first words stops the scroll for buyers.",f:(b,sv)=>b.price&&!/^\[/.test(b.price)?`${cap(b.price)} – ${b.service} ${sv?"i":"in"} ${b.city}.`:null},
  {n:"Honest filter",p:"Honestly: not for everyone. But if you want to [outcome]…",w:"Disqualifying builds trust and calls out the right reader.",f:(b,sv)=>sv?`Ärligt: ${b.name} är inte för alla. Men om du vill ${b.outcome}, läs vidare.`:`Honestly: ${b.name} isn't for everyone. But if you want to ${b.outcome}, read on.`},
  {n:"Local news",p:"New in [city]: [offer].",w:"News + place (only if it really is new).",f:(b,sv)=>sv?`Nytt i ${b.city}: ${b.offer}.`:`New in ${b.city}: ${b.offer}.`},
  {n:"One specific detail",p:"[The single most concrete fact]",w:"The Rolls-Royce move: one precise detail does the selling.",f:(b,sv)=>b.fact},
  {n:"Testimonial (real only)",p:"“[real quote]” – [who]",w:"Social proof — only a real, permitted review. Never invented.",f:(b,sv)=>sv?`”[Riktigt kundcitat, med lov]” – en kund om ${b.service} hos ${b.name}.`:`"[Real customer quote, with permission]" – a customer on ${b.service} at ${b.name}.`},
 ],
 body:[
  {n:"Reason-why",p:"[Fact]\n[Proof]\n[Risk removed]",w:"Three short reasons to believe (Hopkins: reason-why copy).",f:(b,sv)=>`${b.fact}\n${cap(b.proof)}.\n${b.risk}`},
  {n:"Problem → solution (situational)",p:"No need to [friction]. [Fact] [Risk]",w:"Names a situation, not a flaw in the reader — policy-safe for health.",f:(b,sv)=>sv?`Slipp ${b.friction}. ${b.fact} ${b.risk}`:`No need to ${b.friction}. ${b.fact} ${b.risk}`},
  {n:"Before → after → bridge (situational)",p:"Before: [friction]. Now: [outcome]. [Fact]",w:"Shows the change in the reader's day (never body/appearance before–after).",f:(b,sv)=>sv?`Förut: ${b.friction}. Nu: ${b.outcome}. ${b.fact}`:`Before: ${b.friction}. Now: ${b.outcome}. ${b.fact}`},
  {n:"Bullet facts",p:"• [Fact]\n• [Proof]\n• [Risk]",w:"Scannable on a phone; each line is a fact, not an adjective.",f:(b,sv)=>`• ${b.fact}\n• ${cap(b.proof)}\n• ${b.risk}`},
  {n:"1-to-1 letter",p:"Hi [readers]! Here's exactly what you get: [offer]. [Fact] [Risk]",w:"Salesmanship in print: talk to one person (Hopkins).",f:(b,sv)=>sv?`Hej ${b.who}! Så här är det: du får ${b.offer}. ${b.fact} ${b.risk}`:`Hi ${b.who}! Here's exactly what you get: ${b.offer}. ${b.fact} ${b.risk}`},
 ],
 creative:[
  {n:"Real person + offer text",p:"Photo: [real person/place]. Text on image: “[offer]”",w:"Real people from the business beat stock photos; text ≤ 7 words.",f:(b,sv)=>sv?`Foto: ${b.visual}. Text på bilden: ”${cap(b.offer)}”.`:`Photo: ${b.visual}. Text on image: "${cap(b.offer)}".`},
  {n:"Plain offer card",p:"Brand colour, big text: “[offer]” + “[city]”",w:"Plain can win (the Wikipedia text banner test). One message.",f:(b,sv)=>sv?`Enfärgad bakgrund i ${b.name}s färger, stor text: ”${cap(b.offer)}” och ”${b.city}”. Inget annat.`:`Plain background in ${b.name}'s colours, big text: "${cap(b.offer)}" and "${b.city}". Nothing else.`},
  {n:"3-second video",p:"0–3 s: [scene] + text “[reader]: [offer]”",w:"The first 3 seconds decide if they keep watching.",f:(b,sv)=>sv?`Video 0–3 s: ${b.visual}. Textrad: ”${b.who}: ${b.offer}”. 3–10 s: ${lc(b.fact)}`:`Video 0–3 s: ${b.visual}. Text line: "${b.who}: ${b.offer}". 3–10 s: ${lc(b.fact)}`},
  {n:"Show the process",p:"Screen recording: how to [CTA], step by step",w:"Shows how easy the next step is instead of saying it.",f:(b,sv)=>sv?`Skärminspelning med ${b.name}s riktiga sida: så gör du (${lc(nodot(b.cta))}), steg för steg. Text: ”${cap(b.offer)}”.`:`Screen recording of ${b.name}'s real page: how to ${lc(nodot(b.cta))}, step by step. Text: "${cap(b.offer)}".`},
  {n:"Real customer (with permission)",p:"A real customer says in their own words why they chose [name]",w:"Real voice, real person — with written permission. No scripted quotes, no before/after.",f:(b,sv)=>sv?`En riktig kund (med skriftligt lov) berättar med egna ord varför hen valde ${b.name}. Inga manus-citat, inga före/efter-bilder.`:`A real customer (written permission) says in their own words why they chose ${b.name}. No scripted quotes, no before/after images.`},
 ],
 eproof:[
  {n:"Terms as proof",p:"[Fixed price, deadline, guarantee]",w:"When you have no case studies yet, clear terms ARE the proof.",f:(b,sv)=>b.myProof},
  {n:"Their own data",p:"Built on your own [profile/ads]",w:"Proof they can check themselves.",f:(b,sv)=>b.pitch==="meta"?(sv?`Idéerna bygger på era egna omdömen och det ni redan erbjuder — inget påhittat.`:`The ideas are built on your own reviews and what you already offer — nothing made up.`):(sv?`Rapporten bygger på er egen profil: placering, kategorier, bilder och omdömen.`:`The report is built on your own profile: ranking, categories, photos and reviews.`)},
  {n:"Specific observation",p:"One example: [observation]",w:"A specific, checkable detail proves you actually looked.",f:(b,sv)=>b.obs2?(sv?`Ett exempel: ${b.obs2}.`:`One example: ${b.obs2}.`):null},
  {n:"Honest beginner",p:"I'm new, so the risk is on me",w:"Honesty + risk reversal beats pretending to be big.",f:(b,sv)=>sv?`Jag är ny, så jag har fast pris och pengarna-tillbaka-garanti — risken ligger på mig.`:`I'm new, so I work for a fixed price with a money-back guarantee — the risk is on me.`},
 ],
 offer:[
  {n:"Offer + risk removed",p:"[Offer]. [Risk removed]",w:"What they get + why it's safe to say yes.",f:(b,sv)=>`${cap(b.offer)}. ${b.risk}`},
  {n:"Price + what's included",p:"[Service]: [price]. [Fact]",w:"A clear price and one concrete inclusion.",f:(b,sv)=>`${cap(b.service)}: ${b.price}. ${b.fact}`},
  {n:"Risk first",p:"[Risk removed] [Offer] – [CTA]",w:"Leads with safety for nervous buyers.",f:(b,sv)=>`${b.risk} ${cap(b.offer)} – ${lc(nodot(b.cta))}.`},
  {n:"Value list",p:"You get: [offer]\n✓ [fact]\n✓ [risk]",w:"Stacks the concrete parts so the value is visible.",f:(b,sv)=>`${sv?"Du får":"You get"}: ${b.offer}\n✓ ${b.fact}\n✓ ${b.risk}`},
  {n:"Honest limit",p:"[Offer] – valid [real limit you can keep]",w:"Urgency only if it's TRUE. Never invent scarcity.",f:(b,sv)=>sv?`${cap(b.offer)} – gäller [antal/datum du faktiskt kan hålla].`:`${cap(b.offer)} – valid [a number/date you can really keep].`},
 ],
 eoffer:[
  {n:"The sample",p:"I've made [free thing for them]",w:"Hopkins' free sample: give first, ask later.",f:(b,sv)=>sv?`Jag har gjort ${b.emailOffer}.`:`I've put together ${b.emailOffer}.`},
  {n:"Made for them",p:"[Free thing], made for [business] — yours to keep",w:"Personal and no strings.",f:(b,sv)=>sv?`Jag har gjort ${b.offerShort} för just ${b.name} — gratis, och den är din att behålla.`:`I've made a ${b.offerShort} just for ${b.name} — free, and yours to keep.`},
  {n:"No strings",p:"No strings — you don't need to buy anything",w:"Removes the 'what's the catch?' fear.",f:(b,sv)=>sv?`Du får ${b.emailOffer}. Inga krav — du behöver inte köpa något.`:`You get ${b.emailOffer}. No strings — you don't need to buy anything.`},
 ],
 cta:[
  {n:"Action + ease",p:"[CTA].",w:"One action and how easy it is.",f:(b,sv)=>`${nodot(b.cta)}.`},
  {n:"Action + offer",p:"[CTA] – [offer].",w:"Reminds them what they get for acting.",f:(b,sv)=>`${nodot(b.cta)} – ${b.offer}.`},
  {n:"Reason + action",p:"[Risk removed] [CTA].",w:"Removes the last worry right before the click.",f:(b,sv)=>`${b.risk} ${nodot(b.cta)}.`},
  {n:"Reader + action",p:"[Reader situation]? [CTA].",w:"Calls out the reader one last time.",f:(b,sv)=>`${nodot(b.reader)}? ${nodot(b.cta)}.`},
 ],
 ask:[
  {n:"Interest question",p:"Want me to send [it]?",w:"A small yes (Gong: interest CTAs beat meeting asks in cold email).",f:(b,sv)=>b.ask},
  {n:"Worth a look?",p:"Worth a look?",w:"Three words, one-word answer.",f:(b,sv)=>sv?`Är det värt en titt?`:`Worth a look?`},
  {n:"Reply 'yes'",p:"Just reply “yes” and I'll send it.",w:"Tells them the exact, tiny action.",f:(b,sv)=>sv?`Vill du ha den? Svara bara ”ja”.`:`Want it? Just reply "yes".`},
  {n:"Right person?",p:"Should I send it to you, or someone else at [business]?",w:"Easy to answer even if they're not the decision-maker.",f:(b,sv)=>sv?`Ska jag skicka den till dig, eller till någon annan på ${b.name}?`:`Should I send it to you, or to someone else at ${b.name}?`},
 ],
 followup:[
  {n:"One new fact",p:"Hi [name], one more thing: [new observation]. [ask]",w:"Adds value instead of 'just following up'.",f:(b,sv)=>sv?`Hej ${b.owner}, en sak till: ${b.obs2}. ${b.ask}`:`Hi ${b.owner}, one more thing: ${b.obs2}. ${b.ask}`},
  {n:"Easy out",p:"Not a priority? Just say so and I won't email again.",w:"Permission to say no makes replying easy — and respectful.",f:(b,sv)=>sv?`Hej ${b.owner}, jag vill inte tjata. Om ${b.offerShort} inte är aktuellt nu, säg bara till så hör jag inte av mig igen.`:`Hi ${b.owner}, I don't want to pester you. If a ${b.offerShort} isn't a priority right now, just say so and I won't email again.`},
  {n:"Three options",p:"It's probably 1) not now 2) no time 3) buried. Reply with a number.",w:"A one-character reply (the 'reply with a number' pattern).",f:(b,sv)=>sv?`Hej ${b.owner}, jag har inte hört något, så det är nog en av tre saker: 1) inte aktuellt nu, 2) ingen tid än, 3) mejlet drunknade. Svara bara med en siffra.`:`Hi ${b.owner}, I haven't heard back, so it's probably one of three: 1) not a priority, 2) no time yet, 3) my email got buried. Just reply with a number.`},
  {n:"Value first",p:"Here's one of the three things, free: [observation]. Want the other two?",w:"Gives part of the sample right away (Hopkins: give first).",f:(b,sv)=>sv?`Hej ${b.owner}, här är en av de tre sakerna, gratis: ${b.obs2}. Vill du ha de andra två?`:`Hi ${b.owner}, here's one of the three things, free: ${b.obs2}. Want the other two?`},
 ],
 opener:[
  {n:"Observation",p:"Hi [name], [what you saw]",w:"Proves the email is about THEM, in line one.",f:(b,sv)=>`${sv?"Hej":"Hi"} ${b.owner}, ${b.obs}.`},
  {n:"Quick observation",p:"Hi [name], a quick observation about [business]: [what you saw]",w:"Signals 'short and useful'.",f:(b,sv)=>sv?`Hej ${b.owner}, snabb iakttagelse om ${b.name}: ${b.obs}.`:`Hi ${b.owner}, a quick observation about ${b.name}: ${b.obs}.`},
  {n:"How the map works",p:"Hi [name], the top 3 on the map show first; [business] isn't in them",w:"Explains why it matters in one breath.",f:(b,sv)=>b.notTop3?(sv?`Hej ${b.owner}, när någon söker ”${b.kw}” syns de tre första i kartan direkt — resten hamnar under ”Fler platser”. ${b.name} är inte bland de tre.`:`Hi ${b.owner}, when someone searches "${b.kw}", the top 3 on the map show straight away — everyone else is under "More places". ${b.name} isn't in the top 3.`):null},
  {n:"Second observation",p:"Hi [name], [second thing you saw]",w:"A different specific detail — specific beats clever.",f:(b,sv)=>b.obs2?`${sv?"Hej":"Hi"} ${b.owner}, ${b.obs2}.`:null},
 ],
};
function gen(el,b,lang){const sv=lang==="sv";const fb=fillBiz(b,sv);
 if(el==="fullad"){const H=(e,i)=>F[e][i].f(fb,sv)||F[e][0].f(fb,sv);const P=sv?"Primärtext":"Primary text",R=sv?"Rubrik":"Headline",B=sv?"Bild":"Image";
  return [{n:"Reader-first ad",w:"Hook names the reader and the outcome; bullets give facts; one CTA with the offer.",t:`${P}:\n${H("hook",1)}\n${H("body",3)}\n${H("cta",1)}\n${R}: ${H("headline",0)}\n${B}: ${H("creative",0)}`},
   {n:"No-hassle ad",w:"Leads with the friction it removes, then proof, the offer with risk reversal, one CTA.",t:`${P}:\n${H("hook",2)}\n${fb.fact} ${cap(fb.proof)}.\n${H("offer",0)}\n${H("cta",0)}\n${R}: ${H("headline",6)}\n${B}: ${H("creative",2)}`},
   {n:"Proof-first ad",w:"Opens with a checkable fact, then the offer and a last call-out of the reader.",t:`${P}:\n${H("hook",3)}\n${cap(fb.offer)}. ${fb.risk}\n${H("cta",3)}\n${R}: ${H("headline",7)}\n${B}: ${H("creative",1)}`}];}
 if(el==="fullemail")return [0,1,2].map(i=>{const pick=(e,j)=>{const L=F[e].map(x=>x.f(fb,sv)).filter(Boolean);return L[j%L.length];};
  const t=`${sv?"Ämne":"Subject"}: ${pick("subject",[0,3,1][i])}\n\n${pick("opener",[0,2,1][i])}\n\n${pick("eoffer",[0,2,0][i])}\n${pick("eproof",[0,2,3][i])}\n\n${i===1?`${pick("ask",0)} ${sv?"Ett ”ja” räcker.":"A \"yes\" is enough."}`:pick("ask",[0,0,3][i])}\n\n/Oskar${sv?", Synlig Media":", Synlig Media"}`;
  return {n:["Observation → sample → small yes","Map explainer → no-strings → reply yes","Quick observation → honest beginner"][i],w:["The classic: about them, a free sample, one small question.","Explains why it matters, then the easiest possible reply.","Honesty about being new + risk on you."][i],t};});
 return (F[el]||[]).map(x=>({n:x.n,w:x.w,p:x.p,t:x.f(fb,sv)})).filter(x=>x.t);}

from biz import BIZ
ELEMENTS = {
 # id: (channel, level, label, what it is, checker kind)
 "headline":("meta",1,"Meta ad headline","The bold line under the image (short, ~5–10 words). It names the reader or the offer.","headline"),
 "subject":("email",1,"Email subject line","2–6 words. Looks like a normal email from a person, about THEM.","subject"),
 "hook":("meta",2,"Primary text: hook line","The first line of the ad text — the only line people see before 'See more' (keep it under ~125 characters).","hook"),
 "opener":("email",2,"Email first line (opener)","The first sentence after 'Hej Anna'. A specific observation about their business — not about you.","opener"),
 "body":("meta",3,"Primary text: body","2–4 short lines after the hook: reason-why, one fact, one proof.","body"),
 "creative":("meta",3,"Image / creative idea","Describe the picture or the first 3 seconds of video: who, what, where, text on image (max ~7 words).","creative"),
 "eproof":("email",3,"Email proof line","One or two sentences that make your claim believable — specific, checkable, honest.","eproof"),
 "offer":("meta",4,"Ad offer","Exactly what they get, what it costs and what removes the risk.","offer"),
 "eoffer":("email",4,"Email offer","What you give them for free first (the 'sample'), in one sentence.","eoffer"),
 "cta":("meta",5,"Ad call to action","ONE action, with how easy/fast it is.","cta"),
 "ask":("email",5,"Email ask (CTA)","A small yes: an interest question they can answer in one word.","ask"),
 "followup":("email",5,"Follow-up email","Email #2, sent 3–4 days later: short, adds ONE new thing, easy out.","followup"),
 "fullad":("meta",6,"Full Meta ad","Hook + body + offer + CTA + headline + image idea. No hints.","fullad"),
 "fullemail":("email",6,"Full cold email","Subject + opener + offer + proof + ask (+ a P.S. or follow-up). No hints.","fullemail"),
}
LEVELS = [
 dict(n=1,title="Headlines",sub="Meta headlines + email subject lines, with heavy guidance"),
 dict(n=2,title="Hooks",sub="The first line of an ad, the first line of an email"),
 dict(n=3,title="Body, proof & image",sub="Reason-why lines, proof, creative ideas"),
 dict(n=4,title="Offers",sub="What they get, the price, the risk reversal"),
 dict(n=5,title="Calls to action & follow-ups",sub="One action. A small yes. A polite follow-up"),
 dict(n=6,title="Full ad / full email",sub="From a client brief, no hints, optional timer"),
]
EMAILABLE=[b for b in BIZ if b["obs"]]
ADABLE=BIZ
def pickn(lst,n,off): return [lst[(off+i)%len(lst)] for i in range(n)]
REPS=[]
def add(**k):
    k["id"]=f"r{len(REPS)+1:03d}"; REPS.append(k)
PLAN=[("headline",14,0),("subject",12,0),("hook",12,3),("opener",10,4),("body",9,6),("creative",6,11),("eproof",7,8),
      ("offer",9,9),("eoffer",7,2),("cta",7,13),("ask",6,6),("followup",6,1),("fullad",9,5),("fullemail",9,10)]
for el,n,off in PLAN:
    pool=ADABLE if ELEMENTS[el][0]=="meta" else EMAILABLE
    for i,b in enumerate(pickn(pool,n,off)):
        add(mode="guided",el=el,level=ELEMENTS[el][1],biz=b["id"],lang=b["lang"])
# formula drills: one brief, write it in 10 formulas
for el,bid in [("headline","solna-tand"),("headline","expat-dent"),("headline","synlig-map"),("subject","frisk-gym"),("subject","plumb-leeds"),("hook","salong-klipp"),("hook","pt-london"),("hook","fysio-ost")]:
    b=[x for x in BIZ if x["id"]==bid][0]; add(mode="formula",el=el,level=ELEMENTS[el][1],biz=bid,lang=b["lang"])
# 10 versions, star the best
for el,bid in [("headline","trattoria"),("subject","optiker"),("hook","synlig-en"),("offer","yoga"),("ask","bilverk"),("cta","hair-toronto")]:
    b=[x for x in BIZ if x["id"]==bid][0]; add(mode="ten",el=el,level=ELEMENTS[el][1],biz=bid,lang=b["lang"])

# ---- Fix this weak line (TEACHING EXAMPLES: weak lines written for practice) ----
FIX=[
 ("headline","sv","solna-tand","Välkommen till Solna Tandvård – vi brinner för dina tänder!",["Talar om oss, inte läsaren","Floskel ('brinner för') i stället för fakta","Inget erbjudande, ingen siffra"],"Solnabor: tandkontroll för 695 kr – boka på 2 minuter"),
 ("headline","en","hair-toronto","Quality Haircuts by Passionate Professionals",["No reader callout","Platitudes ('quality', 'passionate')","No offer or number"],"Queen West: a sharp cut in 30 minutes, $38"),
 ("headline","sv","laser-gbg","Hatar du dina hårstrån? Bli hårfri på 3 behandlingar!",["Negativ självbild ('hatar du') – bryter mot Metas hälsoregler","Tidslöfte ('på 3 behandlingar') utan förbehåll","Utropstecken = hype"],"Gratis konsultation med provskott – fast pris innan du bestämmer dig"),
 ("subject","sv","frisk-gym","Samarbetsförslag från Synlig Media AB!!",["Handlar om dig, inte dem","Ser ut som reklam (företagsnamn, utropstecken)","Inget om deras verksamhet"],"Johan, plats 5 för ”gym hammarby”"),
 ("subject","en","plumb-leeds","Grow Your Business With Our Proven SEO Services",["Looks like spam (title case, buzzwords)","'Proven' with no proof","Not about Headingley Plumbing"],"plumber headingley"),
 ("hook","sv","trattoria","Vi på Trattoria Lilla Roma är stolta över att presentera vår nya lunchmeny som vi har jobbat med länge.",["Börjar med 'vi' – läsaren är inte med","För långt för en krok (över 100 tecken utan nytta)","Ingen siffra, ingen nytta"],"Kungsholmen: färsk pasta, sallad och kaffe för 135 kr – på 30 minuter."),
 ("opener","sv","fysio-ost","Hej! Jag heter Oskar och driver byrån Synlig Media som hjälper företag att växa digitalt.",["'Jag heter…' – handlar om dig","Inget namn på mottagaren","Ingen iakttagelse om deras klinik"],"Hej Erik, jag sökte på ”fysioterapeut Östermalm” och Östermalms Fysio kom på plats 7 – efter två kliniker med färre omdömen."),
 ("opener","en","cafe-austin","Hope this email finds you well! I wanted to reach out because I help businesses like yours.",["'Hope this finds you well' = filler","'Businesses like yours' = not personal","No observation"],"Hi Rosa, I searched 'breakfast East Austin' and Eastside Bagel Co. came up #5 – with no photos of the bagels."),
 ("body","sv","stad","Vi erbjuder högkvalitativ städning med bred kompetens och flexibla lösningar för alla behov.",["Bara floskler: 'högkvalitativ', 'bred kompetens', 'lösningar'","Inga fakta, inget bevis","Ingen läsare"],"Samma städare kommer varje gång. Priset gäller efter RUT: från 289 kr/timme. Är något inte bra städar vi om inom 24 timmar."),
 ("eproof","sv","hund-uppsala","Vi är Sveriges bästa byrå och garanterar fantastiska resultat för alla våra kunder.",["Påstående utan bevis ('bästa')","'Garanterar fantastiska resultat' – omöjligt att hålla","Hype"],"Rapporten bygger på er egen profil: placering, kategorier, bilder och omdömen. Fixen kostar 4 900 kr och du får pengarna tillbaka om du inte är nöjd."),
 ("offer","sv","yoga","Kom och prova yoga hos oss, vi har många olika klasser.",["Inget konkret erbjudande","Inget pris, ingen risk-sänkning","'Många olika' = vagt"],"2 veckors nybörjarkort för 199 kr. Gillar du det inte efter första passet får du pengarna tillbaka."),
 ("eoffer","en","derm-dublin","We offer a full range of digital marketing services at competitive prices.",["No free first step (sample)","'Full range' and 'competitive' are vague","Asks them to buy before they trust you"],"I've sketched 3 Facebook ad ideas for Ranelagh Skin Clinic that lead with your free consultation – free, yours to keep."),
 ("cta","sv","naprapat-malmo","Kontakta oss gärna för mer information, ring, mejla eller besök vår hemsida!",["Tre olika handlingar = ingen handling","'För mer information' ger ingen anledning","Utropstecken"],"Boka en tid från 07.00 – det tar 2 minuter på nätet."),
 ("ask","sv","bilverk","Har du tid för ett 30 minuters möte på tisdag kl 14 eller onsdag kl 10?",["Stort ja direkt (30 min möte) från en främling","Gong: intresse-CTA slår mötesförfrågan i kalla mejl","Inget värde först"],"Vill du att jag skickar rapporten?"),
 ("followup","en","pt-london","Just following up on my last email. Did you get a chance to read it?",["'Just following up' adds nothing new","Puts guilt on them","No easy out"],"Hi Dan, one more thing: your free starter session is only on page 3 of your website. Should I send the 3 ad ideas that lead with it? If it's not a priority, just say so and I won't follow up again."),
 ("followup","sv","optiker","Hej igen! Bara en påminnelse om mitt förra mejl. Hör av dig!",["'Bara en påminnelse' tillför inget","Ingen ny iakttagelse","Inget enkelt sätt att säga nej"],"Hej Karin, en sak till: er profil saknar knappen för att boka tid direkt. Ska jag skicka rapporten? Är det inte aktuellt, säg bara till så hör jag inte av mig igen."),
]
for el,lang,bid,weak,probs,fix in FIX:
    add(mode="fix",el=el,level=ELEMENTS[el][1],biz=bid,lang=lang,weak=weak,problems=probs,fix=fix)

# ---- Steal like a pro (REAL structures, quoted from cited sources) ----
STEAL=[
 ("headline","sv","solna-tand","caples_piano","\"They Laughed When I Sat Down At the Piano — But When I Started to Play!\" (John Caples, 1926)","De [reaktion] när jag [handling] — men när jag [resultat]!","Story + reversal in one line: a doubt the reader shares, then a surprise.",
  "De skrattade när jag bokade tandläkaren på mobilen – men när jag satt i stolen 2 dagar senare…"),
 ("headline","sv","synlig-map","schwab","\"Do You Make These Mistakes in English?\" (Sherwin Cody course ad, developed with copywriter Maxwell Sackheim; ran for 40+ years)","Gör ni de här [N] misstagen i [område]?","A question that makes the reader check themselves – and promises a specific list.",
  "Gör er klinik de här 3 misstagen i Google-kartan?"),
 ("headline","en","plumb-leeds","kodak","\"You press the button, we do the rest.\" (Kodak, 1889)","You [one tiny action], we do the rest.","Removes effort: the reader's part is tiny, yours is everything else.",
  "You call, we do the rest – a fixed £60 call-out in Headingley"),
 ("hook","en","bilverk","rolls","\"At 60 miles an hour the loudest noise in this new Rolls-Royce comes from the electric clock\" (David Ogilvy, 1958)","[Specific situation] the [surprising detail] comes from [unexpected source].","One concrete, surprising fact proves the whole claim — no adjectives needed.",
  "Bilägare i Täby: det enda du märker av servicen är att bilen står tvättad på uppfarten kl 17."),
 ("opener","en","expat-dent","conroy","\"On a beautiful late spring afternoon, twenty-five years ago, two young men graduated from the same college.\" (Martin Conroy, WSJ letter, mailed 1975–2003)","[Time] [two people/businesses] [started the same]. [Then a difference].","A tiny story comparing two similar people pulls the reader in to find out the difference.",
  "Hi Priya, two dental clinics on Östermalm both have 4.8 stars. Only one shows up when expats search 'English dentist Stockholm'."),
 ("opener","sv","vvs-nacka","skyscraper","\"I was searching for some articles about [Your topic] today and I came across this page: [URL]\" (Brian Dean, Backlinko; 17 links from 160 emails)","Jag sökte på [sökord] i dag och såg att [deras företag] [iakttagelse].","Shows how you found them and that you actually looked — honest, specific personalisation.",
  "Hej Ali, jag sökte på ”rörmokare Nacka” i dag och Nacka VVS-Jour fanns inte bland de tre i kartan."),
 ("offer","sv","frisk-gym","pepsodent","\"FREE… a 10-day tube to everyone who wants white, dazzling teeth\" (Pepsodent, 1929, Claude Hopkins era)","GRATIS: [prov] till alla som vill [önskan].","Hopkins' sample: let people try before they buy — the free first step does the selling.",
  "Gratis: en provvecka på Frisk Gym till alla i Hammarby som vill komma igång – inget kort, inget avtal."),
 ("body","sv","trattoria","gropen","\"Låt mig berätta vad ni får för 25 kronor härnere mellan Gropens vackra pelarvalv\" (Olle Bornefors, Gropen/Palace Hotel, Göteborg)","Låt mig berätta vad ni får för [pris]: [rad för rad, konkreta detaljer]. [Ärlig förbehåll].","1-to-1 salesmanship: one host talks to you, lists every concrete thing you get and is honest about the catch.",
  "Låt mig berätta vad du får för 135 kr: färsk pasta som Marco kavlade i morse, en sallad och en kopp kaffe. Lunchen serveras 11–14."),
 ("ask","sv","nagel","braun","\"If you're interested, just reply and I'll send it along.\" (Josh Braun, as published in Woodpecker's cold email ebook)","Om du vill, svara bara så skickar jag [sak].","The smallest possible yes: no meeting, no call — just 'reply'.",
  "Om du vill, svara bara ”ja” så skickar jag de 3 annonsidéerna."),
 ("followup","sv","yoga","reeder","Bernie Reeder's follow-up: \"I haven't heard back from you and that tells me one of three things: 1)… 2)… 3)…\" (reported 46% reply rate)","Jag har inte hört något, så det är nog en av tre saker: 1) [inte aktuellt] 2) [ingen tid än] 3) [humor]. Svara bara med en siffra.","Makes replying take 2 seconds and gives an easy, friendly no.",
  "Hej Hanna, jag har inte hört något, så det är nog en av tre saker: 1) inte aktuellt nu, 2) ingen tid än, 3) mejlet drunknade. Svara bara med en siffra så vet jag."),
 ("cta","en","synlig-en","wmf5","\"If everyone reading this donated $5, our fundraiser would end today.\" (Wikipedia banner, 2010 test winner)","If [small, specific action] [tiny amount], [clear outcome].","A tiny, specific ask plus a picture of the result beat deadline pressure in a real test.",
  "If you send me your clinic's name, you'll have the report in your inbox within 24 hours."),
 ("fullad","sv","salong-klipp","westermans","Westermans Bar & Restaurant: \"Plain Food & Gourmet Dishes Downstairs. Wine, bar, drinks, snacks, juke box & live music upstairs. Open 17-24, 7 days a week. Old Town. On the corner of Stora Nygatan/Tyska Brinken.\"","[Vad du får här] · [Vad du får där] · [Öppettider] · [Exakt adress].","Pure specifics: what, when, where. The reader can act without any questions.",
  "Klippning på lunchen, 11.30–13.30 varje vardag. 495 kr. Hornsgatan, 2 minuter från Mariatorget. Boka en lunchtid."),
 ("fullemail","en","derm-dublin","harris","Bryan Harris's email to companies he wanted as clients: \"I made a demo for you … to show you what it might look like: <LinkToDemo>. Is this something you guys would be interested in?\"","[Why them] → [proof you do this] → [a sample made for them] → [interest question].","Do a small piece of the work first: the sample is the proof.",
  "Subject: ad ideas for Ranelagh\n\nHi Aoife, I noticed your recent ads use before/after photos, which Meta often restricts for cosmetic treatments. I sketched 3 ad ideas that lead with your free consultation instead – no before/after needed. Should I send them over?"),
 ("fullemail","sv","fysio-ost","kreuzberger","Bryan Kreuzberger: \"I am writing in hopes of finding the appropriate person who handles…\" (subject: \"Appropriate person\")","Ämne: Rätt person · Jag försöker hitta den som ansvarar för [område] · [en mening varför] · Är det du? Annars, vem ska jag fråga?","When you don't know who decides, ask a tiny question that's easy to forward.",
  "Ämne: rätt person\n\nHej, jag försöker hitta den som ansvarar för Östermalms Fysios Google-profil. Jag såg att ni kommer på plats 7 för ”fysioterapeut Östermalm” och har gjort en gratis rapport om varför. Är det du – annars, vem ska jag skicka den till?"),
]
for el,lang,bid,src,quote,skel,why,model in STEAL:
    add(mode="steal",el=el,level=ELEMENTS[el][1],biz=bid,lang=lang,src=src,quote=quote,skeleton=skel,why=why,model=model)
REPS.sort(key=lambda r:(r["level"],["guided","fix","steal","formula","ten"].index(r["mode"]),r["id"]))
for i,r in enumerate(REPS): r["id"]=f"w{r['level']}-{i+1:03d}"
if __name__=="__main__":
    from collections import Counter
    print(len(REPS),Counter(r["level"] for r in REPS),Counter(r["mode"] for r in REPS),Counter(r["el"] for r in REPS))

# Copy & Confidence Workshop

Live: https://oskaraxels.github.io/copy-confidence-workshop/

A free, static practice site (no account, no API, no AI) in three parts:

1. **Copy Workshop** – 167 writing reps over 6 levels (headlines → hooks → body/proof/image → offers → CTAs/follow-ups → full Meta ad / full cold email). Each rep: a teaching brief (Swedish or English) → 5 guided questions → you write → instant rule-based check with a score and prioritised fixes → rewrite with before/after → 3–5 model answers, each a different named formula with "why it works". Extra modes: 10-formula drills, "10 versions, star the best", "fix this weak line", "steal like a pro". "Your own brief" mode generates model answers from what you type. Everything you write goes to the copy bank (score over time, JSON/CSV/Markdown export).
2. **Real Ads Lab** – 74 items: good or bad, then a breakdown of headline, hook, image, offer and CTA. 51 real items quoted with a source (Swedish archive ads, long-running classics, published A/B tests, cold emails published by their authors), 15 live Meta Ad Library search tasks (nothing copied or scraped) and 8 labelled teaching examples.
3. **Belief Builder** – 28 cards (selling the Map Pack fix and Meta ads, sales calls, price, rejection, comparing yourself to friends, discipline, worth). Rate 1–10 before and after; per-card chart. Unlimited, any order.

Home: suggested ~20-minute daily flow (1 belief, 3 ads, 5 reps), daily target (never a cap), streak, dashboard, spaced repetition for misses.

Keyboard: Enter = main action (check → reveal → next) · Ctrl+Enter while typing · 1/2 good/bad · 1–9, 0 rate a belief · C check · R reveal · M done · B save · T timer · ←/→ · F focus · Esc · ?

The Next button always sits in the bottom-right corner, with the answer buttons directly to its left.

Progress lives in your browser (`localStorage` key `ccw-progress-v1`); export/import on the home page.

- Content source: `research/*.py` → `python3 research/build.py` → `data/content.js`, `data/content.json`, `SOURCES.md`
- Tests: `python3 tests/test_site.py <url> <label> [--nolinks] [--shots]` (headless Chrome at 1366×768 and 1440×900 plus a link check)
- Sources and evidence labels: [SOURCES.md](SOURCES.md)

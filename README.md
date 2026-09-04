# Astra Teardown

**Can a language model produce genuinely strategic analysis of an Indonesian
conglomerate from public data — or does it just produce something that *sounds*
strategic?**

This repo is an attempt to answer that honestly. It's a small pipeline that
reads Astra International's public financial results and produces a
consulting-style strategic teardown — and, more importantly, it documents
exactly where the model's analysis is trustworthy and where it quietly falls
apart.

If you only open one file in this repo, open
**[`CRITIQUE.md`](CRITIQUE.md)** — the part that catalogues where the AI got
things wrong and how I caught it. That file is the actual point of this project.

---

## Why this project exists

The prevailing story about AI in professional services is that it automates the
junior analyst — the person who reads the filings, organizes the numbers, and
drafts the first cut of the analysis. I wanted to test that story on a real
example instead of arguing about it in the abstract.

So I picked a hard, specific target: **Astra International**, Indonesia's largest
listed conglomerate — seven divisions spanning cars, motorcycles, heavy
equipment, coal, palm oil, financial services, and more. The kind of sprawling
holding company that is genuinely difficult to analyze, and that sits in a market
(Indonesia) most analysts don't cover closely.

The result is not "AI replaces the analyst" or "AI is useless." It's something
more specific and more useful: **the model is reliable at some analytical tasks
and dangerously unreliable at others, in ways that are predictable once you know
where to look.** Documenting that boundary is what this project is actually about.

---

## What the tool does

It runs as a sequence of stages, each one a separate, purpose-built prompt
against the same source — Astra's FY2024 results:

| Stage | What it produces |
|-------|------------------|
| **Extract** | Pulls segment structure and figures from the source, refusing to invent any number not present in the text |
| **Thesis** | A three-sentence strategic position — the answer-first opening a consulting document leads with |
| **Portfolio Map** | The revenue-vs-profit divergence across segments, as a table plus interpretation |
| **Profit Pools & Dependencies** | What each major profit source depends on, and how fragile that dependency is |

The architecture decision that matters: **the analytical frame is
human-designed; the model fills it.** The sections, the questions each one
answers, and the prompts that enforce consulting-style reasoning are mine. The
extraction and synthesis are the model's. The whole project lives in the gap
between those two things — what the model can do inside a well-designed frame,
and where it still needs a human who understands the business.

---

## The interesting part: where it breaks

This is a scoped project by design. It goes **deep on three sections and on the
question of trust**, rather than thin across a longer checklist of sections. That
was a deliberate call: a teardown where every claim is stress-tested is worth more
than a longer one where the back half is unverified — especially when the entire
value of the exercise is knowing which claims to believe.

The [`CRITIQUE.md`](CRITIQUE.md) appendix documents three real failures the model
produced, why each is wrong, why it matters, and why the model made it. A preview:

- **It blurred two different kinds of risk.** The model grouped Astra's auto
  business and its coal/heavy-equipment business together as "commodity-exposed"
  — but one is exposed to consumer demand and the other to commodity prices.
  Different shocks, blurred into one fluent phrase.
- **It read a growing loan book as a weakness.** The model framed the debt inside
  Astra's financial-services arm as a vulnerability — when for a lending
  business, that debt *is* the engine. Confidently stated, internally coherent,
  and exactly backwards. The most instructive error in the project.
- **It overstated its own best insight.** Correct numbers, but the prose called
  the most *efficient* segment the "earnings engine" — a claim the table directly
  contradicts.

Then the part I'm proudest of: after catching the first two errors, I wrote
guardrails into a later stage's prompt targeting those exact failures — and
**the corrections held.** The commit history records the full loop: error,
diagnosis, encoded fix, fix verified in subsequent output. That loop — model
drafts, human with domain knowledge catches the failure, correction fed back
into the system — is, I think, the actual right way to use these tools for
analytical work.

---

## What I take from it

Three conclusions, stated plainly in the appendix and worth previewing here:

1. **LLMs are reliable at structure, unreliable at interpretation.** They
   organize and draft well; their strategic judgment cannot be trusted unchecked.
2. **The dangerous errors are the fluent ones.** A confident, well-written,
   internally consistent claim is exactly where a subtle inversion hides. Polish
   is not correctness.
3. **Domain knowledge is the bottleneck, not the model.** Every error here was
   catchable only by someone who understands how these businesses actually work —
   which is why analysts who pair AI fluency with real business understanding get
   *more* valuable as this technology spreads, not less.

---

## Running it yourself

```bash
# install dependencies
pip install -r requirements.txt

# add your Anthropic API key to a .env file (see .env.example)
# then run any stage against the source data:
python step3_thesis.py
python step4_portfolio.py
python step5_profit_pools.py
```

The source data (`sample.txt`) is Astra's publicly reported FY2024 figures. No
private or non-public information is used anywhere in this project.

---

## About

Built by **Philip Rickard** — incoming Ivey HBA1 at Western University
(Class of 2028), currently in Capital Markets Finance at OMERS. I grew
up partly in Jakarta and speak Bahasa Indonesia, which is why Astra and the
Indonesian conglomerate landscape are a natural place for me to do this kind of
work — and part of why I think the intersection of AI tooling and regional
business knowledge is underexplored.

I went from not knowing what an API was to building this pipeline. That was the
point: not to show I already knew how to do this, but to show I could learn to.

- **Email:** philrickard88@gmail.com · prickard.hba2028@ivey.ca
- **LinkedIn:** [philip-rickard](https://www.linkedin.com/in/philip-rickard)

*This is v1, focused on Astra. A natural v1.5 — ingesting Bahasa-language
sources, which most tools can't read — is the planned next step, and the one
where the regional-knowledge edge would matter most.*

# Astra Teardown

**Can a language model produce genuinely strategic analysis of an Indonesian
conglomerate from public data, or does it only produce something that *sounds*
strategic?**

This repo is an attempt to answer that honestly. It's a small pipeline that reads
Astra International's public financial results and produces a consulting-style
strategic teardown. More usefully, it documents exactly where the model's
analysis is trustworthy and where it quietly falls apart.

If you open one file here, open **[`CRITIQUE.md`](CRITIQUE.md)**. It catalogues
three real failures the model produced, why each is wrong, and how I caught them.
That file is the actual point of this project.

---

## Repo map

| File | What's in it |
|------|--------------|
| [`CRITIQUE.md`](CRITIQUE.md) | The three documented failures, the diagnosis of each, and the verified fixes. Start here. |
| `sample.txt` | Source data: Astra's publicly reported FY2024 results |
| `step3_thesis.py` | Generates the three-sentence strategic thesis |
| `step4_portfolio.py` | Revenue vs. profit divergence across segments |
| `step5_profit_pools.py` | Profit pool dependencies and how fragile each one is |

---

## Why this project exists

The prevailing story about AI in professional services is that it automates the
junior analyst: the person who reads the filings, organizes the numbers, and
drafts the first cut of the analysis. I wanted to test that story against a real
example rather than argue about it in the abstract.

So I picked a hard target. **Astra International** is Indonesia's largest listed
conglomerate, with roughly Rp331 trillion (about US$20B) of FY2024 revenue across
seven divisions spanning cars, motorcycles, heavy equipment, coal, palm oil, and
financial services. It is a sprawling holding company that is genuinely difficult
to analyze, sitting in a market most analysts don't cover closely. If
AI-generated strategy work degrades anywhere, it should degrade here.

The result is not "AI replaces the analyst" and not "AI is useless." It is
something narrower and more useful: **the model is reliable at some analytical
tasks and dangerously unreliable at others, in ways that become predictable once
you know where to look.** Mapping that boundary is what this project is about.

---

## What the tool does

It runs as a sequence of stages, each a separate purpose-built prompt against the
same source, Astra's FY2024 results:

| Stage | What it produces |
|-------|------------------|
| **Extract** | Pulls segment structure and figures from the source, refusing to invent any number not present in the text |
| **Thesis** | A three-sentence strategic position, the answer-first opening a consulting document leads with |
| **Portfolio Map** | The revenue-vs.-profit divergence across segments, as a table plus interpretation |
| **Profit Pools & Dependencies** | What each major profit source depends on, and how fragile that dependency is |

The architecture decision that matters: **the analytical frame is
human-designed and the model fills it.** The sections, the question each one
answers, and the prompts that enforce consulting-style reasoning are mine. The
extraction and synthesis are the model's. The whole project lives in the gap
between those two things: what a model can do inside a well-designed frame, and
where it still needs a human who understands the business.

---

## The interesting part: where it breaks

This is a scoped project by design. It goes **deep on three sections and on the
question of trust** rather than thin across a longer checklist. That was a
deliberate call. A teardown where every claim is stress-tested is worth more than
a longer one whose back half is unverified, especially when the entire value of
the exercise is knowing which claims to believe.

[`CRITIQUE.md`](CRITIQUE.md) documents all three failures in full. A preview:

- **It blurred two different kinds of risk.** The model grouped Astra's
  automotive business and its heavy equipment / mining / coal business together
  as "commodity-exposed." One is exposed to Indonesian consumer demand and
  credit conditions; the other to seaborne coal prices. Different shocks,
  different timing, different hedges, collapsed into one fluent phrase.
- **It read a growing loan book as a weakness.** The model framed Rp60.2 trillion
  of net debt inside Astra's financial services arm as a leverage position
  constraining the group. For a lending business, that debt *is* the engine: the
  same growth drove financial services net income up 6%. Confidently stated,
  internally coherent, and exactly backwards. The most instructive error here.
- **It overstated its own best insight.** The numbers were right, but the prose
  called financial services the "earnings engine." Financial services delivers
  24% of group profit on 7% of revenue, which makes it the most capital-efficient
  segment, not the largest. Heavy equipment (35%) and automotive (33%) each
  generate more in absolute terms. The table directly below the sentence
  contradicted it.

Every one of these is the model choosing the more fluent sentence over the more
precise one. In all three cases the arithmetic was right and the interpretation
was where it broke.

Then the part that made the project worth finishing: after catching the first two
errors, I wrote guardrails into a later stage's prompt targeting those exact
failure modes, and **the corrections held.** The commit history records the full
loop of error, diagnosis, encoded fix, and fix verified in subsequent output.
That loop, where the model drafts and a human with domain knowledge catches the
failure and feeds the correction back into the system, is the right way to use
these tools for analytical work.

---

## What I take from it

1. **LLMs are reliable at structure and unreliable at interpretation.** They
   organize and draft well. Their strategic judgment cannot be trusted unchecked.
2. **The dangerous errors are the fluent ones.** A confident, well-written,
   internally consistent claim is exactly where a subtle inversion hides. Polish
   reads as correctness, and isn't.
3. **Domain knowledge is the bottleneck, not the model.** Every error here was
   catchable only by someone who understands how a lending business makes money,
   or how a commodity division differs from a consumer one. Which suggests
   analysts who pair AI fluency with real business understanding get *more*
   valuable as these tools spread, not less.

---

## Scope and limitations

One company, three errors, one reviewer. That is an anecdote, not evidence. I
think the fluency-over-precision pattern generalizes, because there is a
plausible mechanism behind it, but I haven't demonstrated that and won't claim
it. The honest scope is this: on one hard analytical target, the model's failures
clustered in interpretation rather than arithmetic, and were catchable by someone
with domain knowledge and effectively invisible without it.

Whether that holds on a different conglomerate is the next thing to test.

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

Built by **Philip Rickard**, an HBA1 at the Ivey Business School, Western
University (Class of 2028). I spent summer 2026 in Capital Markets Finance at
OMERS. I grew up partly in Jakarta and speak Bahasa Indonesia, which is why Astra
and the Indonesian conglomerate landscape are a natural place for me to do this
kind of work, and part of why I think the intersection of AI tooling and regional
business knowledge is underexplored.

I went from not knowing what an API was to building this pipeline. That was the
point: not to show I already knew how, but to show I could learn how.

- **Email:** prickard.hba2028@ivey.ca · philrickard88@gmail.com
- **LinkedIn:** [philip-rickard](https://www.linkedin.com/in/philip-rickard)

*This is v1, focused on Astra. A natural v1.5, ingesting Bahasa-language sources
that most tools can't read, is the planned next step and the one where the
regional-knowledge edge would matter most.*

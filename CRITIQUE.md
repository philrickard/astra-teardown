Method & Model Critique

An honest account of where the tool's analysis was sound, where it failed, and
what those failures reveal about using LLMs for strategic work.

This appendix is the most important part of the project. The teardown itself
demonstrates that an LLM can produce consulting-shaped output from public
financial data. This section demonstrates something harder and more valuable:
judgment about where that output can and cannot be trusted. Every error
below was caught by reviewing the tool's own output against the source data and
against how these businesses actually work.


How the pipeline works

The tool runs in stages, each a separate prompt against the same source
(Astra International's FY2024 results):


Extract (step2) — pulls the segment structure and figures out of the
source text, under a strict rule to write "not in source" rather than
estimate any missing number.
Thesis (step3) — synthesizes a three-sentence strategic position.
Portfolio Map (step4) — organizes the revenue/profit divergence into a
table plus a short interpretation.
Profit Pools & Dependencies (step5) — reasons about what each major
profit source depends on and how fragile that dependency is.


The structure, section definitions, and prompts are human-designed. The
extraction and synthesis are the model's. That division of labor is the point:
the analytical frame is mine; the model fills it, and I check it.


The central finding: reliability is not uniform

The single most useful thing this project surfaced is that an LLM's
reliability varies sharply by task type, and the variance is predictable:


Structured organization (the Portfolio Map) — highly reliable. When the
model is arranging figures that are explicitly in the source, it does not
invent numbers and does not misorganize them. Across the build, every
figure in the structured sections traced back correctly to the source.
Interpretation and synthesis (the Thesis, the dependency reasoning) —
reliable on facts, but prone to framing errors: claims that are internally
coherent, confidently stated, and subtly wrong. These are the dangerous ones,
because they read as authoritative.


This asymmetry shaped where I concentrated review effort: lightly on the
structured sections, heavily on the interpretive ones. That is the practical
lesson — not "AI is unreliable," but "AI is unreliable in specific, locatable
ways, and the job is knowing where to look."


The errors, in detail

Error 1 — Conflating two different kinds of cyclicality

Where: The Thesis section.
What the model wrote: It grouped Automotive and HEMCE together as "cyclical,
commodity-exposed businesses."
Why it's wrong: These are two genuinely different risk types. HEMCE (coal,
heavy equipment, nickel) is commodity-cyclical — its profit tracks seaborne coal
prices and global commodity demand. Automotive is consumer-demand cyclical —
its profit tracks Indonesian household purchasing power and credit conditions,
not commodity prices. Blurring them into one phrase ("commodity-exposed") is
wrong about Automotive and obscures the real structure of the group's risk.
Why it matters: The distinction is the whole point of a dependency analysis.
A group exposed to two different shocks is more diversified than one exposed to
the same shock twice. Collapsing the two makes the risk picture look simpler — and
different — than it is.
Why the model made it: "Cyclical and commodity-exposed" is a fluent,
cohesive-sounding phrase. The model optimized for a clean sentence and let two
distinct ideas collapse into one. This is the characteristic LLM failure: prose
fluency overriding analytical precision.

Error 2 — Reading a growing loan book as a weakness

Where: The Thesis section.
What the model wrote: It framed the Rp60.2 trillion of net debt inside
Astra's financial services subsidiaries as a vulnerability — a "leverage
position that constrains its capacity to serve as a true shock absorber."
Why it's wrong: For a consumer-finance business, debt is not a warning sign —
it is the raw material. These businesses borrow in order to lend; the debt funds
the loan book that generates the profit. The source is explicit that the debt
grew because the loan book grew, and that the same growth drove financial
services net income up 6%. The model took a number that signals the business
working as designed and reframed it as fragility.
Why it matters: This is the most dangerous error in the project, because it
is confidently stated, internally consistent, and exactly backwards. Anyone who
understands how a lending business works would catch it; anyone who doesn't would
be actively misled by it. It is the clearest demonstration of why domain judgment
cannot be outsourced to the model.
Why the model made it: The Thesis prompt asked for a strategic position with
a point of view. The model built a coherent bearish thesis, and a large debt
number is rhetorically convenient for a bearish thesis — so it got recruited into
the argument regardless of what it actually meant. The model reasoned from
narrative coherence, not from how the business works.

Error 3 — "Earnings engine" vs. most efficient segment

Where: The Portfolio Map section.
What the model wrote: The numbers in the table were flawless, but the
interpretation leaned on calling financial services Astra's "real earnings
engine."
Why it's wrong: Financial services delivers 24% of group profit on 7% of
revenue — making it the most capital-efficient segment, the one that punches
furthest above its revenue weight. But it is not the largest profit source:
HEMCE (35%) and Automotive (33%) each generate more absolute profit. "Earnings
engine" implies biggest contributor; the data says most efficient contributor.
Those are different claims.
Why it matters: It's a subtler error than the first two — the math is right
and the underlying observation (FS is remarkably efficient) is real. But the
framing overstates the case in a way the table directly contradicts. A careful
reader comparing the prose to the numbers would notice the tension.
Why the model made it: "Most efficient" is a quieter claim than "earnings
engine." The model reached for the more dramatic framing because it makes a
punchier sentence — again, fluency over precision.


The part that worked: encoding the fixes

The three sections were not built blind. After catching Errors 1 and 2 in the
Thesis, I wrote explicit guardrails into the Profit Pools prompt
(step5) targeting those exact failures:


A rule instructing the model to distinguish consumer-demand cyclicality from
commodity cyclicality, and not blur them.
A rule stating that for a consumer-finance business, a growing debt-funded loan
book is the business model working, not inherently a fragility.


Both guardrails held. The Profit Pools output explicitly separated the two
cyclicality types ("This is a consumer-demand cyclicality risk, not a commodity
risk") and correctly framed the financial services debt ("the business model
functioning as designed — funded lending — not inherently a structural
fragility"). The commit history records this sequence: error, diagnosis,
encoded fix, fix verified.

This is the most important result in the project. It shows the right workflow for
LLM-assisted analysis: the model drafts, a human with domain knowledge catches
the failures, and the corrections are fed back into the system so the failure
doesn't recur. The value is not the model and not the human in isolation — it is
the loop between them.


What this implies for AI in strategy work

Three takeaways, stated plainly:


LLMs are reliable at structure, unreliable at interpretation. Use them to
organize and draft; do not trust their strategic judgment unchecked.
The dangerous errors are the fluent ones. A model's confident, coherent,
well-written claim is exactly where a subtle inversion can hide. Polish is not
correctness.
Domain knowledge is the bottleneck, not the model. Every error here was
catchable only by someone who understands how these businesses work. The model
is a force multiplier on judgment, not a substitute for it — which is precisely
why AI-fluent analysts who also understand the underlying business are more
valuable as this technology spreads, not less.


The teardown shows the tool can produce the output. This appendix shows I know
when to believe it.
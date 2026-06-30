"""
step5_profit_pools.py — Section 3: Profit Pools & Dependencies.

This is the THIRD and final section we're building. It completes the arc:
- Thesis (step3): what the company is
- Portfolio Map (step4): where revenue and profit diverge
- Profit Pools (step5): what each profit source DEPENDS ON, and how fragile

This is synthesis-heavy, like the Thesis — which means HIGHER error risk than
the Portfolio Map. The model has to reason about dependencies and fragilities,
not just arrange numbers. Expect it to say something that sounds sharp but
needs your judgment to verify. That's the point — this section will likely
generate the richest entries for your critique appendix.

NEW IDEA: this prompt asks the model to reason about RISK and DEPENDENCY,
which is inherently interpretive. We counter the error risk by forcing it to
ground every dependency claim in a specific fact from the source — so a
reader (you) can check each one.
"""

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

with open("sample.txt", "r", encoding="utf-8") as f:
    source_text = f.read()

PROFIT_POOLS_PROMPT = """You are a strategy consultant writing Section 3 of a \
teardown of an Indonesian conglomerate: PROFIT POOLS & DEPENDENCIES.

The Portfolio Map (prior section) already established WHERE profit comes from. \
This section answers the harder question: what does each major profit pool \
critically DEPEND ON, and how fragile is that dependency?

For the THREE largest profit contributors only (by profit share), produce one \
entry each, in this format:

**[Segment name] — [profit share]% of group profit**
- *Depends on:* the 1-2 specific external factors this segment's profit hinges \
on (e.g. a commodity price, a licensing relationship, an interest rate \
environment, consumer demand).
- *Fragility read:* one sentence on how exposed this is — is the dependency \
diversified or concentrated, structural or cyclical?

Then close with one paragraph titled "**The dependency picture:**" (3-4 \
sentences) on whether the group's profit pools are correlated (all exposed to \
the same shock) or genuinely diversified.

RULES:
- Every "Depends on" claim must be grounded in a SPECIFIC fact in the source. \
If the source mentions Toyota/Honda licensing, coal prices, CPO prices, \
consumer finance loan books — use those. Do not invent dependencies the \
source doesn't support.
- Distinguish carefully between CONSUMER-DEMAND cyclicality (e.g. car sales \
tracking purchasing power) and COMMODITY cyclicality (e.g. coal/CPO prices). \
These are different risks — do not blur them into one.
- For a consumer-finance business, remember that a growing loan book funded by \
debt is the business model working, not inherently a fragility. Frame it \
accurately.
- No invented numbers. Every figure must appear in the source.

<source>
{text}
</source>"""

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": PROFIT_POOLS_PROMPT.format(text=source_text)}
    ],
)

print("=" * 60)
print("SECTION 3 — PROFIT POOLS & DEPENDENCIES")
print("=" * 60)
print(message.content[0].text)
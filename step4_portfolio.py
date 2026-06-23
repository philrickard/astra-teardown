"""
step4_portfolio.py — Section 2: The Portfolio Map.

CONTRAST WITH step3:
- step3 (Thesis) = pure synthesis. High value, high error risk. The model
  invents a *view*, and views can be subtly wrong (remember the financial-
  services-debt mistake).
- step4 (Portfolio Map) = structured organization. Low error risk. The model
  arranges numbers that are explicitly in the source. Much harder to get wrong.

This contrast is deliberate and it's an interview point: the tool's
reliability is NOT uniform across sections. The structured sections are
trustworthy; the interpretive sections need human review. Designing the
critique effort around that asymmetry is the judgment story.

NEW IDEA: this prompt asks for a specific OUTPUT FORMAT (a markdown table
plus a short "so what"). Forcing format is how you make a pipeline's
sections stitch together cleanly later.
"""

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

with open("sample.txt", "r", encoding="utf-8") as f:
    source_text = f.read()

PORTFOLIO_PROMPT = """You are a strategy consultant building Section 2 of a \
teardown of an Indonesian conglomerate: THE PORTFOLIO MAP.

The job of this section is to show what businesses the group is actually in, \
and to surface the single most important structural fact: how revenue share \
and profit share DIVERGE across segments. That divergence is where strategic \
insight lives.

Produce, in this exact order:

1. A markdown table with columns: Segment | Revenue Share | Profit Share | \
Read. The "Read" column is a 3-6 word characterization (e.g. "scale engine, \
thin margin" or "small but highly profitable").

2. Then one short paragraph (3-4 sentences max) titled "**What the map \
shows:**" that calls out the most important divergence between revenue and \
profit concentration — and what it implies about where the group really \
makes its money.

RULES:
- Use ONLY figures present in the source. Every percentage must appear in \
the source below. Do not invent or estimate.
- If a segment's revenue or profit share isn't given, write "n/a" — never \
guess.
- Be specific and concrete. No filler.

<source>
{text}
</source>"""

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=800,
    messages=[
        {"role": "user", "content": PORTFOLIO_PROMPT.format(text=source_text)}
    ],
)

print("=" * 60)
print("SECTION 2 — THE PORTFOLIO MAP")
print("=" * 60)
print(message.content[0].text)
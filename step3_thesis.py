"""
step3_thesis.py — your first ANALYZE stage.

Extraction (step 2) pulled facts. This stage does something harder: it
takes those facts and produces STRATEGIC PROSE — Section 1 of the
teardown, "The Thesis."

The entire craft is in the prompt below. Read it. The rules are what
force the model to produce a *view* instead of a *summary* — and those
rules are the part you designed, the part you explain in interviews.
"""

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

# ---- Read the same Astra source ----
with open("sample.txt", "r", encoding="utf-8") as f:
    source_text = f.read()

# ---- The Thesis prompt. THIS is the design work. ----
# Every rule here exists to push the model away from "describe the
# company" and toward "take a position a consultant would defend."
THESIS_PROMPT = """You are a strategy consultant writing the opening of a \
client-ready teardown of an Indonesian conglomerate. You write the way BCG \
or McKinsey opens a document: the answer first, no background throat-clearing.

Write Section 1 — THE THESIS: exactly three sentences capturing this \
company's core strategic position.

RULES that separate a thesis from a summary:
- Take a POSITION. A thesis has a point of view someone could disagree \
with — not "the company operates in several sectors" (a fact) but "the \
company's profitability is dangerously concentrated in two cyclical \
businesses" (a claim).
- Lead with the single most important strategic truth, not the largest \
revenue line.
- Every sentence must say something a smart reader couldn't have guessed \
from the company's name alone.
- Use ONLY facts grounded in the source below. No invented numbers. If you \
reference a figure, it must appear in the source.
- No hedging words: avoid "may", "could", "potentially", "arguably". State \
it.
- Three sentences. Not four. Tight.

<source>
{text}
</source>

Output only the three sentences. No heading, no preamble."""

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=400,
    messages=[
        {"role": "user", "content": THESIS_PROMPT.format(text=source_text)}
    ],
)

print("=" * 60)
print("SECTION 1 — THE THESIS")
print("=" * 60)
print(message.content[0].text)
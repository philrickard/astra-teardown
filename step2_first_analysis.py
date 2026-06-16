"""
step2_first_analysis.py — your first REAL pipeline stage.

This is a miniature version of the Extract stage from our architecture:
it takes actual Astra annual report text (which you paste into sample.txt)
and asks the model to pull out the segment structure — with a strict rule
against inventing numbers.

That one rule ("not in source") is your first hallucination control.
Remember it: it's an interview talking point.
"""

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

# ---- 1. Read the source text you pasted in ----
with open("sample.txt", "r", encoding="utf-8") as f:
    source_text = f.read()

if len(source_text.strip()) < 200:
    raise SystemExit(
        "sample.txt looks empty. Paste a few pages of Astra's annual report "
        "(the business segment overview section) into it first."
    )

# ---- 2. The prompt. This is the part YOU design. ----
EXTRACTION_PROMPT = """You are the extraction stage of a strategic-analysis \
pipeline that produces consulting-style teardowns of Indonesian conglomerates.

From the annual report excerpt below, extract:
1. Every business segment named.
2. Revenue and profit figures per segment, if present — include units, \
currency, and year.
3. One sentence per segment on what management says about its strategy.

STRICT RULES:
- Use ONLY information in the provided text.
- If a figure is not in the text, write "not in source". Never estimate, \
never fill gaps from general knowledge.
- Output: a markdown table (segment | revenue | profit), then the strategy \
sentences as a bulleted list.

<annual_report_excerpt>
{text}
</annual_report_excerpt>"""

# ---- 3. The API call ----
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1500,
    messages=[
        {"role": "user", "content": EXTRACTION_PROMPT.format(text=source_text)}
    ],
)

print(message.content[0].text)

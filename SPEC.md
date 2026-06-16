# Output Spec — Indonesian Conglomerate Teardown Tool

**Status:** approved v1 · June 2026
**First target:** Astra International (IDX: ASII)

## What the tool produces

A ~2,000-word strategic teardown in markdown. Design principle: a
*descriptive* report says what a company is; a *strategic* teardown says
where the money is made, what's threatened, and what to watch. Every
section is framed as a question, because questions force analysis.

## The six sections

| # | Section | Question it must answer |
|---|---------|------------------------|
| 1 | The Thesis | The company's strategic position in three sentences |
| 2 | Portfolio Map | What businesses, and how do revenue vs. profit differ by segment? |
| 3 | Profit Pools & Dependencies | Which segments fund the group, and what does each critically depend on? |
| 4 | Strategic Tensions | What 3–4 forces threaten the current model? |
| 5 | Management's Story vs. the Numbers | Does capital allocation match the narrative? |
| 6 | Watchlist | 5 indicators to track over 24 months |

Plus an appendix (repo-only): **Method & Model Critique** — how the
pipeline works, and annotated examples of where the model was right,
wrong, or missing local context.

## Deliberate scope decisions

- **No recommendations section.** LLM-generated strategy advice about a
  company nobody here has worked at is hollow; the Watchlist gives
  forward-looking value without faking authority.
- **English-only sources for v1.** Bahasa-language ingestion is the
  named v1.5 feature.
- **v1 sources: annual report only.** News and IDX filings come later.

## Pipeline architecture

Ingest (PDF → text) → Extract (structured facts, low-temperature
prompts) → Analyze (one tailored LLM call per section) → Assemble
(stitched markdown + sources appendix).

Structure, section definitions, and prompts are human-designed; the
extraction and synthesis are the model's. That division of labor is the
point of the project.

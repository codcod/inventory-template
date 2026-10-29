# /s-query

Answer a question about the inventory using the structured records, with citations
back to source.

## Instructions

Follow the workflow in `agent/prompts/query_prompt.md`.

1. Read `MANIFEST.md` first as the index; identify relevant entries.
1. Open only the relevant `library/entries/<id>.md` records.
1. Answer concisely, citing each claim to its entry (`[[id]]`) and, where relevant,
   the originating `library/raw/` note via `source_notes`.
1. Separate facts from inferences; flag low-confidence records.
1. Offer to file durable, reusable answers under `library/outputs/` — but only if
   asked.

## Constraints

- Read-only. Never invent figures; if data is missing, say what would need to be
  captured.

## See also

- `agent/prompts/query_prompt.md`

# Query

## Purpose

Answer a question about the inventory by navigating the structured records rather than
loading everything into context. Mirrors the "query" operation of the LLM-wiki
pattern: read the index first, open only the relevant records, synthesize, and cite
sources.

______________________________________________________________________

## When to use

- The maintainer or a team asks a question about the inventory, e.g.:
  - "Which teams are working on X?"
  - "Which entries share a dependency on Y?"
  - "Show every active entry that has not been updated in a quarter."
  - "Who owns entries in category Z?"

______________________________________________________________________

## Step-by-step instructions

### 1. Read the index

Read `MANIFEST.md` first. It is the catalog of every entry. Use it to identify which
records are relevant to the question. Do not brute-force read every file.

### 2. Read targeted records

Open only the `library/entries/<id>.md` files the index flags as relevant. Read
frontmatter and the body sections needed to answer.

### 3. Synthesize with citations

Answer concisely. Cite every claim back to its source:

- Link the entry as `[[<id>]]` or `[link](library/entries/<id>.md)`.
- Where a claim originates in a note, trace it to the `library/raw/` file via
  `source_notes`.

Separate facts from inferences. Flag low-confidence records explicitly (the
`confidence` field) and note where an answer depends on unverified self-reported data.

### 4. Offer to file durable answers

If the answer is non-trivial and likely to be asked again (e.g. a cost roll-up or a
cross-team map), offer to save it as `library/outputs/query-<slug>-YYYY-MM-DD.md` so
the knowledge compounds. Do not file it unless asked.

______________________________________________________________________

## Constraints

- Read-only on `library/raw/`, `library/entries/`, and `MANIFEST.md`.
- Never invent figures. If the inventory lacks the data, say so and point to the blank
  fields or missing entries that would need to be filled to answer.
- Prefer "I can answer X from the inventory; Y is not captured yet" over a confident
  but unsupported answer.

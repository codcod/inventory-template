# Lint

## Purpose

Health check on the inventory's data integrity — the "lint" operation of the LLM-wiki
pattern. Distinct from `/s-patterns`: lint checks whether the data is correct and
consistent; patterns interprets the data for consolidation strategy. Run lint
regularly to keep the wiki trustworthy.

______________________________________________________________________

## When to use

- Weekly, or before running `/s-patterns` or answering an important query.
- After bulk edits, imports, or deletions.

______________________________________________________________________

## Checks

Run every check below over `library/entries/`, `library/raw/`, `MANIFEST.md`, and
`CHANGELOG.md`.

### 1. Missing or invalid frontmatter

- Required fields blank: `id`, `name`, `status`, `category`.
- `status` / `category` / `confidence` / `lifecycle_stage` values outside the allowed
  sets defined in `agent/templates/entry_template.md` and
  `agent/context/product-delivery-lifecycle.md`.
- Duplicate `id` across two files (conflict — must be resolved before anything else).
- For entry files whose filename begins with a numeric prefix (`NNN-slug.md`): verify
  that the `id` frontmatter value matches the filename exactly (e.g. file
  `003-pr-review.md` must have `id: 003-pr-review`). Flag any mismatch.
- Duplicate numeric prefixes across two or more files — each number must be unique.

### 2. Manifest drift

- A row in `MANIFEST.md` whose cells do not match the current frontmatter of its file.
- An entry file with no manifest row, or a manifest row with no file.
- `Last updated` / `Total entries` header out of date.

Recommend running `/v-ingest` or `/v-manifest-sync` to fix drift.

### 3. Staleness

- `status: active` with `date_updated` older than 60 days → confirm still active.
- `status: active`, older than 90 days, empty Outcomes → likely stalled.

### 4. Source-note integrity

- `source_notes` referencing a `library/raw/` file that does not exist (dangling
  reference).
- `library/raw/` files not referenced by any entry (un-ingested input — candidate for
  `/v-ingest`).

### 5. Cross-reference integrity

- `related: [[id]]` pointing to an entry id that does not exist (broken link).
- One-directional links: A lists B in `related` but B does not list A → suggest making
  it bidirectional, or removing if it is not a real relationship.
- Orphan records: no `related` links and not referenced by any other record (may be
  genuinely standalone, or may need linking).

### 6. Contradictions

- A frontmatter value contradicting the body (e.g. `status: active` but body says
  paused).
- Two records stating conflicting facts about the same tool, team, or owner.
- A record contradicting its own source note(s) in `library/raw/`.

Report contradictions explicitly; do not resolve them silently.

### 7. Confidence

- List records with `confidence: low` or blank `confidence` that have
  `status: active` — these most need validation.

______________________________________________________________________

## Output

Write the result to `library/outputs/lint-YYYY-MM-DD.md` with sections matching the
checks above, each listing concrete findings (file, field, recommended fix) or "no
issues found". Append a one-line summary to `CHANGELOG.md`.

______________________________________________________________________

## Constraints

- Read-only on `library/raw/`, `library/entries/`, and `MANIFEST.md`. Lint reports
  problems; it does not fix them. Recommend the fixing command (`/v-ingest`,
  `/v-manifest-sync`, or a manual edit).
- If the inventory is empty, say so and skip the report.

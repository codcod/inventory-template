# /v-manifest-sync

Rebuild `MANIFEST.md` from the current frontmatter of every file in
`library/entries/`. Use this after editing entry records directly — it does not read
`library/raw/` or modify any entry file.

## When to use

- After correcting or updating one or more `library/entries/<id>.md` files by hand.
- After deleting or renaming an entry file.
- After pulling changes to `library/entries/` from git.
- To verify the manifest accurately reflects the current state of all records.

Do not use when new notes have been dropped in `library/raw/` — use `/v-ingest`
instead, which runs a manifest sync as its final step.

## Instructions

Follow the workflow in `agent/prompts/manifest_sync_prompt.md`.

1. Read the YAML frontmatter of every `library/entries/*.md` file (skip `.gitkeep`).
1. Build one table row per entry, sorted by `category` then `name`.
1. Rewrite `MANIFEST.md` entirely — update `Last updated`, `Total entries`, the table,
   and the "Summary by category" counts. Preserve any content under `## Notes`.
1. Print a one-line confirmation and list any warnings (parse errors, blank required
   fields, duplicate ids).

## Constraints

- Read-only on `library/raw/` and `library/entries/`. Only `MANIFEST.md` is written.
- If two entry files share the same `id`, flag the conflict and do not write the
  manifest until it is resolved.

## See also

- `agent/prompts/manifest_sync_prompt.md` — full step-by-step rules
- `/v-ingest` — use instead when new or updated notes exist in `library/raw/`

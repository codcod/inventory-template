# /v-ingest

Scan `library/raw/` for notes that have not yet been processed, create or update the
corresponding `library/entries/` records, and regenerate `MANIFEST.md`.

## Instructions

Follow the workflow documented in `agent/prompts/ingest_raw_note_prompt.md` exactly.

Key steps:

1. Identify files in `library/raw/` not yet referenced in any `source_notes`
   frontmatter field across `library/entries/`.
1. For each unprocessed note, match it to an existing entry (two or more signals:
   name, owner/team, tags, problem) or treat it as a new one. Ask before merging if
   uncertain.
1. Create `library/entries/<NNN-slug>.md` from the template (new) or update the
   existing record. For new entries, assign the next available numeric prefix (scan
   existing filenames for the highest `NNN-` number, increment by one, zero-pad to
   three digits). Fill all inferable frontmatter fields; leave the rest blank. Never
   invent data.
1. Regenerate `MANIFEST.md` from all current frontmatter — sorted by category then
   name.
1. Print a changelog: notes scanned, entries created vs. updated, fields left blank,
   overlaps detected, questions raised.

## Constraints

- Do not edit files in `library/raw/`.
- Do not store information only in `MANIFEST.md`.
- Blank fields are correct when data is absent — do not use placeholders.

## See also

- `agent/prompts/ingest_raw_note_prompt.md` — full step-by-step workflow
- `agent/prompts/manifest_sync_prompt.md` — rebuild manifest without ingesting new
  notes
- `agent/templates/entry_template.md` — canonical entry shape

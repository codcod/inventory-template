# Ingest Raw Note → Entry + Manifest

## Purpose

Convert one or more free-form notes from `library/raw/` into structured entry records
in `library/entries/`, then regenerate `MANIFEST.md`. This is the primary operating
loop of the inventory.

______________________________________________________________________

## Inputs

- One or more files in `library/raw/` that are not yet referenced in any
  `source_notes` list in `library/entries/`.
- Existing entry files in `library/entries/` (for matching).
- `MANIFEST.md` (will be fully regenerated at the end).

______________________________________________________________________

## Step-by-step instructions

### 1. Identify unprocessed notes

Read every file in `library/raw/` (skip `.gitkeep`). For each file, search all
`library/entries/*.md` frontmatter for its path in the `source_notes` list. Files not
found anywhere are new inputs to process.

### 2. Match each note to an existing entry or flag as new

For each unprocessed note:

a. Extract the core signals: entry name (or working title), owner, team, tags (tools,
platforms) mentioned, and the problem described in one sentence.

b. Scan `library/entries/` for a record where at least two of the following align:

- Name or working title
- Owner or team
- Primary tag (tool, platform, dependency)
- Problem statement (semantically similar)

c. If a confident match (two or more signals align): treat as an **update** to the
existing record.

d. If no confident match: treat as a **new** entry.

e. If ambiguous (one signal matches weakly): ask a single clarifying question before
proceeding. Do not guess.

### 3a. Create a new entry record

1. Assign a unique numeric identifier and slug:
   a. Scan all existing filenames in `library/entries/` for the pattern `NNN-*` (three
   or more digits followed by a hyphen) to find the highest number currently in use.
   b. Increment that number by one and zero-pad to three digits. If no numbered files
   exist, start at `001`.
   c. Choose a short, stable, lowercase slug (hyphens, no spaces). Example:
   `pr-review`.
   d. Combine as `NNN-slug` — this becomes both the `id` frontmatter value and the
   filename. Example: `003-pr-review` → `library/entries/003-pr-review.md`.
   e. If the raw note provides an `entry_id` field with a numeric component, use it
   only if that number is not already taken; otherwise assign the next available
   number.
1. Copy `agent/templates/entry_template.md` as the starting point.
1. Fill frontmatter fields from the note:
   - Fill every field you can infer with reasonable confidence.
   - Leave a field blank (empty value) if the note does not supply it.
   - Do not invent data. Do not guess at status or category without evidence.
   - `category` must be one of the values listed in the entry template.
1. Populate body sections from the note's content. Keep each section concise.
1. Set `date_created` and `date_updated` to today's date (YYYY-MM-DD).
1. Set `source_notes` to a list containing the raw file path.
1. Under "Open Questions / Follow-ups", list any fields left blank and what
   information would be needed to fill them.

### 3b. Update an existing entry record

1. Open the matched `library/entries/<id>.md`.
1. For each frontmatter field the note provides: update the value only if the new
   information is more precise or more recent than what is already there.
1. If the note contradicts an existing field value, do not silently overwrite. Add a
   note under "Open Questions / Follow-ups" describing the contradiction and asking
   for clarification.
1. Append or revise body sections where the note adds new information.
1. Refresh `date_updated` to today.
1. Append the new raw file path to `source_notes` (preserve existing entries).

### 4. Regenerate MANIFEST.md

Follow `agent/prompts/manifest_sync_prompt.md` steps 1–4.

### 5. Report the changelog

Print a concise summary:

```
Ingest complete — YYYY-MM-DD

Notes scanned:     N
Entries created:   N  (list slugs)
Entries updated:   N  (list slugs)
Fields left blank: list entry IDs and fields
Overlaps detected: describe any newly noticed overlaps
Questions raised:  list any clarifying questions that need answers
```

______________________________________________________________________

## Constraints

- Never edit files in `library/raw/`. They are read-only inputs.
- Never store information only in `MANIFEST.md`. The entry file is the source of
  truth.
- Blank is always correct when information is absent. Do not fill fields with
  placeholders like "TBD" or "unknown."
- When in doubt about a match, ask — do not assume.

# Manifest Sync

## Purpose

Rebuild `MANIFEST.md` entirely from the frontmatter of every file in
`library/entries/`. Run this whenever entry records have been edited directly (not via
`/v-ingest`), or to verify the manifest is in sync with the underlying records.

______________________________________________________________________

## When to use

- After manually editing one or more `library/entries/*.md` files.
- After deleting or renaming an entry file.
- After a bulk import or migration.
- To audit whether the manifest accurately reflects current entry state.

______________________________________________________________________

## Step-by-step instructions

### 1. Read all entry frontmatter

Open every file in `library/entries/` (skip `.gitkeep` and any non-`.md` file). Parse
the YAML frontmatter block (between `---` delimiters). If a file's frontmatter cannot
be parsed, log a warning and skip it — do not abort the full sync.

### 2. Build the table

For each entry, produce one table row using this mapping:

| Column   | Frontmatter field | Notes                             |
| -------- | ----------------- | --------------------------------- |
| ID       | `id`              | Use as-is                         |
| Entry    | `name`            | Use as-is                         |
| Owner    | `owner`           | Blank cell if empty               |
| Team     | `team`            | Blank cell if empty               |
| Status   | `status`          | Blank cell if empty               |
| Category | `category`        | Blank cell if empty               |
| Updated  | `date_updated`    | Blank cell if empty               |
| Detail   | link              | `[link](library/entries/<id>.md)` |

Sort rows: primary by `category` (alphabetical, blank values sort last), secondary by
`name` (alphabetical).

### 3. Build the category summary

Count entries per category. List each category with its count, sorted alphabetically.
Example:

```
- category-a: 3
- category-b: 2
- category-c: 1
```

If a category field is blank, count those under `(uncategorized)`.

### 4. Write MANIFEST.md

Rewrite the full file using this structure:

```markdown
# Inventory Manifest

> Single source of truth for all entries in the inventory. Regenerated from
> `library/entries/*.md` frontmatter. Do not edit rows by hand — update the underlying
> entry file and re-run `/v-ingest` or `/v-manifest-sync`.

Last updated: YYYY-MM-DD · Total entries: N

| ID | Entry | Owner | Team | Status | Category | Updated | Detail |
| -- | ----- | ----- | ---- | ------ | -------- | ------- | ------ |
| ... one row per entry ... |

## Summary by category

- category: N
- ...

## Notes

[preserve existing content here]
```

Update `Last updated` to today's date. Update `Total entries` to the count of rows.
Preserve all existing content under `## Notes`.

### 5. Report

Print a one-line confirmation:

```
Manifest synced — YYYY-MM-DD · N entries · N categories
```

List any warnings (files skipped due to parse errors, blank required fields).

______________________________________________________________________

## Constraints

- Do not edit entry files during a manifest sync — this workflow is read-only on
  `library/entries/`.
- The manifest must be fully derived from frontmatter. Do not add information to the
  manifest that is not in the underlying files.
- If two entry files have the same `id`, flag the conflict and do not write the
  manifest until it is resolved.

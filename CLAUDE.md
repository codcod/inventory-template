# CLAUDE.md

## Repository Purpose

This repository is an inventory operated by Claude Code. Its goal is to give its
readers a single, up-to-date view of every tracked entry (project, initiative,
experiment, tool — whatever you choose to inventory) and to surface overlaps and
consolidation opportunities that isolated efforts would otherwise miss.

The repository contains:

- `library/raw/` — free-form notes dropped by the maintainer or contributors (immutable)
- `library/entries/` — one structured record per entry (YAML frontmatter + body)
- `MANIFEST.md` — the central table and index, regenerated from frontmatter
- `CHANGELOG.md` — append-only operation log (audit trail)
- `library/outputs/` — dated lint, pattern, and query reports
- `agent/prompts/` — reusable workflow prompts for each operation
- `agent/templates/` — entry template (agent-internal; defines the schema)
- `library/templates/` — input templates for contributors
- `agent/context/` — reference knowledge the agent reads but never modifies; currently
  holds the lifecycle model
- `.claude/commands/` — slash commands wiring the workflows

______________________________________________________________________

## Customization

Before first use, adapt these to your domain:

- **Categories** — list the allowed `category` values in
  `agent/templates/entry_template.md`. That file is the single source of truth for the
  schema; prompts and docs refer to it.
- **Lifecycle** — replace the example stages in
  `agent/context/product-delivery-lifecycle.md` with your own. If you change stage
  slugs, also update `PHASE_*` constants in `tools/generate_pdf.py` and the slug lists
  in `library/templates/raw_note_template.md`.
- **Integrations** — set the Confluence page ID and GitLab URL under
  `## Integrations` below.

______________________________________________________________________

## Operating Model

This repo follows the LLM-wiki pattern: `library/raw/` is immutable source,
`library/entries/` is the generated knowledge layer you maintain, and `MANIFEST.md` is
the index you read first to navigate. You do almost all the writing; humans mostly
read.

Commands, each exposed as a slash command:

- `/v-ingest` (write) — turn new/changed `library/raw/` notes into entry records and
  refresh `MANIFEST.md`.
- `/v-manifest-sync` (write, light) — rebuild `MANIFEST.md` from current frontmatter
  only; use after editing entry files directly without running `/v-ingest`.
- `/s-query` (read) — answer questions from the inventory with citations.
- `/v-lint` (read + report) — check data integrity; write a dated report to
  `library/outputs/`.
- `/s-patterns` (read + report) — surface consolidation opportunities; write a report
  to `library/outputs/`.
- `/s-opportunities` (read + report) — compare entry coverage against the lifecycle
  model and surface stages with no or thin coverage.
- `/v-confluence-sync` (write, external) — push the current inventory table to a
  Confluence page. See `## Integrations` for the target page ID.
- `/v-gitlab-fetch` (write) — fetch a GitLab project summary into `library/raw/`.

After every state-changing operation (`/v-ingest` or `/v-manifest-sync`), append an
entry to `CHANGELOG.md`. Never rewrite past log entries.

______________________________________________________________________

## Ingest Workflow — raw note → entry + manifest

This is the core operating loop. Run it via `/v-ingest`.

### Step 1 — Scan library/raw/

Read every file in `library/raw/`. For each file, check whether it is already
referenced in any `source_notes` list inside `library/entries/`. Files not referenced
anywhere are **new inputs**.

### Step 2 — Match or create

For each new input, decide:

- **Existing entry**: the note describes something already in `library/entries/`.
  Match on entry name, owner/team, tags, and the problem described. A confident match
  requires at least two of these to align.
- **New entry**: the note does not match any existing record with confidence.

When unsure, ask one brief clarifying question rather than silently merging or
duplicating. Prefer clarity over speed.

If the note filename contains `_update_` (e.g. `2026-07-01_update_pr-review.md`),
treat it as a guaranteed update to an existing record — never create a new entry from
it. If no existing entry matches with confidence, ask one clarifying question to
identify the right record before proceeding.

### Step 3 — Write the entry record

For a **new** entry:

1. Assign a unique numeric identifier:
   - Scan filenames in `library/entries/` for the `NNN-*` pattern to find the highest
     number in use. Increment by one, zero-padded to three digits. Start at `001` if
     none exist.
   - Choose a short stable lowercase slug (hyphens, no spaces), e.g. `pr-review`.
   - The `id` is `NNN-slug` (e.g. `003-pr-review`). The filename matches:
     `003-pr-review.md`.
   - If the raw note supplies an `entry_id`, use its numeric component if free;
     otherwise assign the next available number.
1. Create `library/entries/<id>.md` using `agent/templates/entry_template.md`.
1. Fill all frontmatter fields you can infer from the note. Leave fields blank if the
   note does not supply them — do not invent data.
1. Set `confidence` based on how well-verified the note is: `high` (corroborated or
   measured), `medium` (single credible source), `low` (hearsay or speculative).
1. Set `related` to `[[id]]` links for any existing entry this one overlaps with (same
   category plus a shared tag or problem). When you add a link from A to B, also add
   the reverse link in B and refresh B's `date_updated` so the graph stays
   bidirectional.
1. Set `lifecycle_stage` to the stage(s) from
   `agent/context/product-delivery-lifecycle.md` that best match what this entry does.
   Read the context file if not already loaded. Use the slugs defined there. If no
   stage clearly fits, leave blank and note in "Open Questions."
1. Set `docs` to any documentation links the note mentions (Confluence pages, wikis)
   and `source` to any source-code or source-file links (repos, boards, design files).
   Capture the full URL. Leave blank if the note supplies none.
1. Populate the body sections from the note's content.
1. Set `date_created` and `date_updated` to today. Set `source_notes` to the raw file
   path.

For an **existing** entry:

1. Update frontmatter fields where the note provides new or more precise information.
1. Re-evaluate `confidence` as corroboration arrives, and update `related` links if
   the note reveals a new overlap.
1. Append or revise the relevant body sections.
1. Refresh `date_updated` to today.
1. Append the new raw file path to `source_notes` (do not remove existing entries).

Never edit files in `library/raw/`. They are immutable inputs.

### Step 4 — Regenerate MANIFEST.md

After all entry files are written or updated:

1. Read the frontmatter of every file in `library/entries/` (skip `.gitkeep`).
1. Build one table row per entry, sorted by `category` then `name`.
1. Rewrite `MANIFEST.md` entirely, updating the row count and `Last updated` date.
1. Rebuild the "Summary by category" section with counts.
1. Preserve any manually added notes in the `## Notes` section.

### Step 5 — Append to CHANGELOG.md

Append a dated entry to `CHANGELOG.md` recording: scope (notes processed), created
ids, updated ids, and notable findings (contradictions, overlaps, blanks, questions).
Do not modify earlier entries.

### Step 6 — Report

Print a short changelog:

- How many raw notes were scanned.
- How many entries were created vs. updated.
- Any newly detected overlaps or consolidation candidates.
- Any fields that were left blank due to missing information.
- Any open questions that need human input.

If the report contains non-trivial findings — overlaps, consolidation candidates, open
questions, or contradictions — save the full printed summary as a new file in
`library/raw/` (e.g. `library/raw/YYYY-MM-DD_ingest-findings.md`) immediately after
printing it. The printed summary is ephemeral; only `CHANGELOG.md` gets a high-level
entry automatically. Saving it to `library/raw/` ensures the findings are picked up on
the next `/v-ingest`, cross-referenced against entry records, and preserved in the
audit trail.

______________________________________________________________________

## Manifest Regeneration Rules

`MANIFEST.md` is always derived from `library/entries/*.md` frontmatter. Never store
information only in the manifest table. The authoritative record is the entry file.

Column mapping: ID→`id`, Entry→`name`, Owner→`owner`, Team→`team`, Status→`status`,
Category→`category`, Updated→`date_updated`,
Detail→`[link](library/entries/<id>.md)`.

Sort: primary by `category` (alphabetical), secondary by `name` (alphabetical).

`lifecycle_stage`, `problem`, `tags`, `confidence`, `related`, `docs`, and `source`
are intentionally not manifest columns; they are surfaced through `/s-query`,
`/v-lint`, and the Obsidian frontend (graph view + Dataview). The `docs` and `source`
links let a user or agent jump straight to an entry's documentation or source
artifacts when they need more detail.

______________________________________________________________________

## Cross-References (`related`)

Entry records link to each other with `related: [[id]]` wikilinks. These links are the
backbone of the consolidation goal: opened as an Obsidian vault, the `related` graph
shows clusters of overlapping entries at a glance.

Rules:

- Add a `related` link when two entries share a category and either a tag or a
  problem.
- Keep links bidirectional: if A links B, B links A.
- Use the entry `id` inside the wikilink (e.g. `[[003-pr-review]]`).
- `/v-lint` checks for broken links (pointing to a missing id) and one-directional
  links.

______________________________________________________________________

## Pattern Detection — Consolidation Signals

When running `/s-patterns`, look for:

- **Shared tags**: multiple entries in the same category sharing tags (tools,
  dependencies, platforms). Flag as "shared tooling opportunity."
- **Duplicate problems**: two or more entries addressing the same underlying pain with
  different approaches. Flag as "consolidation candidate."
- **Stalled entries**: entries with `status: active` older than 90 days with no
  evidence of outcomes. Flag for review.
- **Coverage gaps**: categories with only one entry vs. categories with five or more.
  Note imbalance.

Separate confirmed overlaps from suspected ones. Use language like "likely overlap —
confirm with owners" for uncertain cases. File the report under `library/outputs/`.

______________________________________________________________________

## Data Health — Lint

`/v-lint` checks the inventory for integrity problems: missing or invalid frontmatter,
manifest drift, stale records, dangling or un-ingested `library/raw/` notes, broken or
one-directional `related` links, contradictions, and low-confidence active records. It
writes a dated report to `library/outputs/` and recommends fixes — it never edits
records itself. Full rules: `agent/prompts/lint_prompt.md`.

______________________________________________________________________

## Query

`/s-query` answers questions about the inventory. It reads `MANIFEST.md` as the index,
opens only the relevant records, and synthesizes an answer with citations back to the
entry and originating `library/raw/` note. It never invents figures; if the data is
not captured, it says so. Full rules: `agent/prompts/query_prompt.md`.

______________________________________________________________________

## Lifecycle Context

`agent/context/product-delivery-lifecycle.md` defines the lifecycle the inventory is
mapped against: its stages, with activities, typical roles, and typical artefacts for
each. The agent uses this as a reference frame for two purposes:

1. **During `/v-ingest`**: populate `lifecycle_stage` on new entry records by matching
   the entry's problem and approach to the lifecycle stages.
1. **During `/s-opportunities`**: compare the entry landscape against the full
   lifecycle to surface stages with thin or no coverage.

Rules:

- Read `agent/context/product-delivery-lifecycle.md` before any operation that
  requires lifecycle reasoning.
- Use the stage slugs exactly as they appear in the context file.
- `agent/context/` files are never edited by the agent. If the lifecycle changes, the
  user updates the context file directly and re-runs `/v-ingest` to refresh
  assignments.

______________________________________________________________________

## Signal and Uncertainty Handling

- If a raw note mentions a person or team without enough context to fill the `owner`
  or `team` field confidently, leave it blank and add an item under "Open Questions."
- If a note describes something that sounds like two separate entries, note the
  ambiguity and ask the maintainer before splitting.
- Never invent status or category. Blank is correct when the information is absent.
- Set `confidence` honestly. A polished record built from one unverified message is
  still `low` confidence. `/v-lint` surfaces low-confidence active records for
  validation.
- When a note contradicts an existing entry record (e.g. different owner or status),
  note the contradiction explicitly rather than silently overwriting.

______________________________________________________________________

## Writing Guidance

- Be concise. Avoid corporate jargon.
- Separate facts from opinions and inferences.
- Explicitly flag uncertainty ("unclear from note", "not confirmed").
- Prefer evidence-based conclusions in the body sections.
- Keep the manifest readable: short values, no prose in table cells.
- Headings in entry files follow the template — do not add or rename sections without
  updating the template.

______________________________________________________________________

## Integrations

### Confluence sync

Target page ID: <CONFLUENCE_PAGE_ID>

`/v-confluence-sync` reads this page ID and updates a section titled "Inventory —
auto-synced" on that page. It never creates a new page. To configure: replace the
placeholder above with the numeric Confluence page ID (visible in the page URL as
`?pageId=XXXXXXX` or in the page's share settings).

### GitLab

Base URL: https://gitlab.com

`/v-gitlab-fetch` uses this URL as the API root. Replace the value above with your
self-hosted GitLab URL if applicable (e.g. `https://gitlab.mycompany.com`).

Authentication: the `GITLAB_TOKEN` environment variable must be set to a personal
access token with `read_api` scope. The agent never reads or logs the token value.

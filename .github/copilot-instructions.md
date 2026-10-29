# Copilot Instructions — inventory

This repository is an AI-operated knowledge base for tracking inventory entries.
Claude Code is the primary operator; this file guides editor assistants (GitHub
Copilot, etc.) on repo conventions and intent.

______________________________________________________________________

## Repository layout

```
MANIFEST.md              # Generated central table — never edit rows by hand
CLAUDE.md                # Agent operating instructions
CHANGELOG.md             # Append-only operation log — never rewrite past entries
agent/
  prompts/               # Workflow prompts for each operation
  context/               # Reference knowledge — lifecycle model; agent reads, never edits
  templates/             # Entry template (agent-internal; defines the schema)
library/
  raw/                   # Immutable drop zone for unstructured notes
  entries/               # One structured record per entry (source of truth)
  outputs/               # Dated reports from /v-lint, /s-patterns, /s-opportunities
  templates/             # Input templates for contributors
tools/                   # Executable scripts and automation
.claude/commands/        # Slash commands
```

______________________________________________________________________

## Frontmatter schema

Every `library/entries/<id>.md` file opens with the YAML frontmatter block defined in
`agent/templates/entry_template.md`. Follow its field order and allowed values
exactly; the allowed `category` values and `lifecycle_stage` slugs are defined there
and in `agent/context/product-delivery-lifecycle.md`.

Leave a field blank rather than inventing a value. Do not add fields not listed in the
template.

______________________________________________________________________

## Body sections

Every entry record has these fixed sections in this order. Do not rename, reorder, or
add sections:

1. Summary
1. Problem & Motivation
1. Approach
1. Current State
1. Outcomes & Evidence
1. Risks & Constraints
1. Consolidation Opportunities
1. Open Questions / Follow-ups

______________________________________________________________________

## Commands

The repository is operated through slash commands in Claude Code. Do not invoke these
manually or simulate their output:

| Command              | What it does                                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------- |
| `/v-ingest`          | Processes new `library/raw/` notes into entry records and refreshes `MANIFEST.md`               |
| `/v-manifest-sync`   | Rebuilds `MANIFEST.md` from current frontmatter; use after direct edits to `library/entries/`   |
| `/v-lint`            | Health-checks data integrity; writes a dated report to `library/outputs/`                       |
| `/v-confluence-sync` | Pushes the entry table to the configured Confluence page                                        |
| `/v-gitlab-fetch`    | Fetches a GitLab project summary into `library/raw/`                                            |
| `/s-query`           | Answers questions from the inventory with citations                                             |
| `/s-patterns`        | Surfaces overlaps and consolidation candidates; writes a report to `library/outputs/`           |
| `/s-opportunities`   | Maps entry coverage against the lifecycle model; writes a report to `library/outputs/`          |

______________________________________________________________________

## Markdown conventions

- Line wrap: **88 characters** (`just fmt` runs `mdformat --wrap 88`).
- Newline at end of every file. LF line endings. UTF-8.
- Concise headings; structured bullets; tables only where they add scannable value.
- No corporate jargon. Separate facts from interpretation. Flag uncertainty
  explicitly.

______________________________________________________________________

## Do not suggest

- Editing rows directly in `MANIFEST.md` — it is always regenerated.
- Editing any file in `library/raw/` — immutable source inputs.
- Editing any file in `agent/context/` — reference knowledge maintained by humans, not
  the agent.
- Appending to or rewriting past entries in `CHANGELOG.md`.
- Adding frontmatter fields not listed in the entry template.
- Filling blank frontmatter fields with placeholder values like "TBD" or "unknown."
- Reordering or renaming entry body sections.
- Creating one-directional `related` links — if A links B, B must link A.

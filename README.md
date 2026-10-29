# inventory-template

A template for an inventory operated by Claude Code. Drop raw notes; the agent
maintains the structured knowledge.

## What this is

Teams work on related things independently. This repository captures every entry —
project, initiative, experiment, tool, whatever you choose to track — in one place so
readers can see the full landscape, spot duplicated effort, and identify consolidation
opportunities.

The central artifact is **`MANIFEST.md`** — a single table derived from the structured
records in `library/entries/`. Always regenerated from source; do not edit it by hand.

______________________________________________________________________

## Getting started

1. Create a repository from this template.
1. Define your categories in `agent/templates/entry_template.md` (the `category`
   field).
1. Replace the example lifecycle in `agent/context/product-delivery-lifecycle.md` with
   your own (or keep it).
1. Optional integrations — set the values under `## Integrations` in `CLAUDE.md`:
   - Confluence page ID for `/v-confluence-sync` (uses the Atlassian MCP server in
     `.mcp.json`).
   - GitLab base URL for `/v-gitlab-fetch` (needs `GITLAB_TOKEN`).
1. Optional PDF report (`just pdf`) — needs `pandoc`, `xelatex`, and a `.venv` with
   `pyyaml` (`python3 -m venv .venv && .venv/bin/pip install pyyaml`).

See `## Customization` in [CLAUDE.md](CLAUDE.md) for details.

______________________________________________________________________

## How to add an entry

1. Create a file in `library/raw/` — any name, any format. Write a brief description:
   what it does, who owns it, what tools it uses, what problem it solves. A few
   sentences is enough. Use `library/templates/raw_note_template.md` as a guide.
1. Run `/v-ingest` in Claude Code. The agent creates or updates the matching record,
   links related entries, regenerates `MANIFEST.md`, and logs the operation.
1. Review the generated record in `library/entries/<id>.md`. If anything is wrong,
   correct the file directly and run `/v-manifest-sync`.

To update an **existing** entry, use `library/templates/raw_note_update_template.md`
instead — it is lighter and signals the agent to update rather than create.

______________________________________________________________________

## How to correct a record

Edit `library/entries/<id>.md` directly — it is the source of truth, not the manifest.
Then run `/v-manifest-sync` to rebuild `MANIFEST.md`.

If your correction contradicts the original raw note, drop a short correction note
into `library/raw/` so the agent won't re-infer the wrong value on the next
`/v-ingest`.

See [docs/inventory.md](docs/inventory.md) for field-by-field guidance.

______________________________________________________________________

## Explore the inventory

| Command            | What it does                                                                                  |
| ------------------ | --------------------------------------------------------------------------------------------- |
| `/s-query`         | Answers questions with citations — who owns what, which teams share which dependencies, etc.  |
| `/s-patterns`      | Surfaces overlaps, duplicated effort, and consolidation candidates across all entries.        |
| `/s-opportunities` | Maps entry coverage against the lifecycle; highlights stages where coverage is thin.          |

______________________________________________________________________

→ Layout, all operator commands, cadence, and principles:
**[docs/inventory.md](docs/inventory.md)**

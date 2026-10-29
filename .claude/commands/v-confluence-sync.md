# /v-confluence-sync

Push the current MANIFEST.md entry table to the designated Confluence page. Use after
`/v-ingest` or `/v-manifest-sync` when you want the Confluence page to reflect the
latest inventory state.

## When to use

- After any operation that changes `MANIFEST.md` (`/v-ingest`, `/v-manifest-sync`).
- On demand, to bring the Confluence page up to date without re-running a full
  ingest.

Do not use if `MANIFEST.md` is stale — run `/v-manifest-sync` first.

## Instructions

Follow the workflow in `agent/prompts/confluence_sync_prompt.md`.

1. Read `MANIFEST.md` and extract the five sync columns: id, entry, owner, status,
   category.
1. Read the target page ID from `CLAUDE.md § Integrations`.
1. Fetch the current Confluence page (version number + body).
1. Build a Confluence storage-format table for the extracted rows.
1. Replace the `Inventory — auto-synced` section if present, or append it.
1. Call `mcp__atlassian__updateConfluencePage` with the merged body.
1. Append a one-line entry to `CHANGELOG.md`.

## Constraints

- Read-only on all local files except `CHANGELOG.md`.
- One external write: `mcp__atlassian__updateConfluencePage`.
- Never create a new Confluence page — only update the configured one.
- Never invent or transform data beyond reformatting for Confluence storage format.
- If the page ID is not set in `CLAUDE.md`, stop and ask the user to add it.

## See also

- `agent/prompts/confluence_sync_prompt.md` — full step-by-step rules
- `CLAUDE.md § Integrations` — target page ID configuration
- `/v-manifest-sync` — use to refresh MANIFEST.md before syncing

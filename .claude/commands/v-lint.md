# /v-lint

Run data-integrity health checks across the inventory and write a dated report.

## Instructions

Follow the workflow in `agent/prompts/lint_prompt.md`. Checks:

1. Missing/invalid frontmatter, duplicate ids.
1. Manifest drift vs. current frontmatter.
1. Stale records (active > 60d; active > 90d with no outcomes).
1. Source-note integrity (dangling refs; un-ingested raw notes).
1. Cross-reference integrity (broken/one-directional `related` links; orphans).
1. Contradictions (frontmatter vs body; record vs record; record vs source note).
1. Active, low-confidence records needing validation.

Write findings to `library/outputs/lint-YYYY-MM-DD.md` and append a one-line summary
to `CHANGELOG.md`.

## Constraints

- Read-only on `library/raw/`, `library/entries/`, `MANIFEST.md`. Lint reports; it
  does not fix. Recommend `/v-ingest`, `/v-manifest-sync`, or a manual edit for each
  issue.

## See also

- `agent/prompts/lint_prompt.md`

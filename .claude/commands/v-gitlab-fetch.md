# /v-gitlab-fetch

Fetch a GitLab project and write a structured note to `library/raw/`, ready for
`/v-ingest`.

## When to use

When the user provides a GitLab project path (e.g. `mygroup/myproject`) or numeric
project ID and wants it captured as an entry candidate in this inventory.

## Instructions

### Step 1 — read config

Read the GitLab base URL from `CLAUDE.md § Integrations → GitLab`. Default to
`https://gitlab.com` if not set.

### Step 2 — run the fetch

```sh
python3 tools/gitlab_fetch.py <project-path-or-id> --gitlab-url <base-url>
```

If the script exits with a missing-token error, stop and tell the user:

> `GITLAB_TOKEN` is not set. Export a personal access token with `read_api` scope:
>
> ```sh
> export GITLAB_TOKEN=glpat-xxxxxxxxxxxx
> ```

HTTP 404 or 403 means the token lacks access — report and stop.

### Step 3 — confirm output

Read the final `Written: library/raw/...` line and tell the user the path of the note.

### Step 4 — offer to ingest

Ask whether to run `/v-ingest` immediately or leave the note in `library/raw/` for
later review. If the user confirms, run `/v-ingest`.

## Constraints

- Do not edit the generated note beyond what the script wrote.
- Do not fabricate project details; the note contains only what the API returned.

## See also

- `tools/gitlab_fetch.py` — fetch script
- `CLAUDE.md § Integrations → GitLab` — base URL configuration
- `/v-ingest` — turns raw notes into structured entry records

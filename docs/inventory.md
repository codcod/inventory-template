# Inventory reference

Detailed reference for the inventory repository. For the quick-start, see
[README.md](../README.md).

______________________________________________________________________

## Layout

```
inventory/
├── MANIFEST.md              # Master table + index — regenerated, do not edit manually
├── CLAUDE.md                # How the agent operates this repo
├── CHANGELOG.md             # Append-only operation log (audit trail)
├── agent/                   # AI reasoning layer
│   ├── prompts/               # Reusable workflow prompts
│   ├── context/               # Reference knowledge — lifecycle model and domain context
│   └── templates/             # Entry template (agent-internal; defines the schema)
├── library/                 # The knowledge base — source of truth
│   ├── raw/                   # DROP ZONE — paste unstructured notes here (immutable)
│   ├── entries/               # One structured .md record per entry
│   ├── outputs/               # Dated lint, pattern, and query reports
│   └── templates/             # Input templates for contributors
├── tools/                   # Executable scripts and automation
└── .claude/commands/        # Slash commands
```

______________________________________________________________________

## Lifecycle context

`agent/context/product-delivery-lifecycle.md` defines the lifecycle the inventory is
mapped against — stages with activities, typical roles, and artefacts for each. The
template ships with a generic five-stage example (Idea, Discovery, Ideation,
Development & Delivery, GTM); replace it with your own. The agent uses it as the
reference frame for all gap and opportunity analysis.

Every entry record carries a `lifecycle_stage:` frontmatter field mapping it to one or
more stages. The `/s-opportunities` command reads both the context file and the entry
landscape to identify where coverage is thin or absent.

To update the lifecycle model, edit `agent/context/product-delivery-lifecycle.md`
directly and run `/v-ingest` so the agent can re-evaluate `lifecycle_stage`
assignments on any records that may be affected.

______________________________________________________________________

## All commands

### Inventory operator commands (`v-`)

| Command              | Source                             | What it does                                                                                                                            |
| -------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `/v-ingest`          | `library/raw/`                     | Reads new/changed notes, creates or updates entry records, then rebuilds `MANIFEST.md`.                                                 |
| `/v-manifest-sync`   | `library/entries/`                 | Rebuilds `MANIFEST.md` from current frontmatter only. Use after editing entry files directly — does not read `library/raw/`.             |
| `/v-lint`            | `library/entries/`, `library/raw/` | Health-checks data integrity (missing fields, drift, staleness, broken links, contradictions) and writes a dated report to `library/outputs/`. |
| `/v-confluence-sync` | `MANIFEST.md`                      | Pushes the current entry table to the configured Confluence page.                                                                       |
| `/v-gitlab-fetch`    | GitLab API                         | Fetches a GitLab project summary into `library/raw/`, ready for `/v-ingest`.                                                            |

The key distinction between the two write commands:

- **Something changed in `library/raw/`** → `/v-ingest` (full pipeline: notes →
  records → manifest).
- **Something changed in `library/entries/`** → `/v-manifest-sync` (last step only:
  records → manifest).

### Exploration commands (`s-`)

| Command            | What it does                                                                                                                       |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `/s-query`         | Answers questions about the inventory with citations. Reads `MANIFEST.md` as the index, opens only relevant records.               |
| `/s-patterns`      | Surfaces overlaps, duplicated effort, and consolidation candidates; writes a dated report to `library/outputs/`.                   |
| `/s-opportunities` | Maps entry coverage against the lifecycle model; surfaces stages with no or thin coverage; saves a dated report to `library/outputs/`. |

### `just` targets

| Target           | What it does                                                                         |
| ---------------- | ------------------------------------------------------------------------------------ |
| `just clean-all` | Removes all generated records and reports; resets `MANIFEST.md` and `CHANGELOG.md`. |
| `just pdf`       | Builds a PDF report in `library/outputs/` (needs pandoc, xelatex, `.venv` + pyyaml). |
| `just fmt`       | Formats markdown to 88 columns with `mdformat`.                                      |

______________________________________________________________________

## Operating cadence

- New note dropped in `library/raw/` → run `/v-ingest`.
- Entry file edited directly → run `/v-manifest-sync`.
- A question about the landscape → run `/s-query`.
- Weekly → run `/v-lint`, then `/s-patterns`.
- Before a planning cycle → run `/s-opportunities`.
- After any manifest change → run `/v-confluence-sync` (if configured).

______________________________________________________________________

## Correcting a record — field by field

The agent infers frontmatter fields from raw notes. If its interpretation is wrong,
edit `library/entries/<id>.md` directly. The entry file is the source of truth; the
manifest is a derived projection. Never edit `MANIFEST.md` directly.

After any direct edit, run `/v-manifest-sync` to rebuild the manifest.

Common corrections:

- **`status`** — correct to `paused` or `abandoned` if the entry has stalled since the
  source note was written.
- **`category`** — move the entry to a better-fitting category.
- **`confidence`** — raise it if you have direct knowledge the agent lacked; lower it
  if an outcome claim is less reliable than it looks.
- **`owner` / `team`** — fill in a last name, correct an attribution, or assign an
  owner where the agent left it blank.
- **`related`** — add a `[[id]]` link if the agent missed an overlap, or remove one if
  the connection isn't real. Keep links bidirectional: if you add A→B, also add B→A.
- **`tags`** — clarify a tool name or add one that was omitted.

Allowed values for each field are listed in `agent/templates/entry_template.md`.

### Correcting or expanding the body

Open `library/entries/<id>.md` and edit the relevant section (Summary, Approach,
Outcomes, Risks, Consolidation Opportunities, or Open Questions). Update
`date_updated` to today. Body-only changes don't require `/v-ingest` unless you also
want the manifest header timestamp refreshed.

### If your correction contradicts the raw note

The agent re-reads `library/raw/` on every `/v-ingest`. If you correct a field that it
would re-infer incorrectly from the original source, drop a short correction note into
`library/raw/` so the right interpretation is on record and won't be overwritten:

```
# Correction: <entry-id> — YYYY-MM-DD

This note corrects the record for <entry name>.

- status is <correct value>, not <inferred value>: [your reason].
- owner is <person>: [how you know, e.g. "confirmed directly with team"].
- confidence raised to medium: outcomes have since been independently verified.
```

The agent will pick this up on the next `/v-ingest`, update the record, and append the
correction to `CHANGELOG.md`. The original raw note is left untouched.

______________________________________________________________________

## Principles

- **The manifest is derived, not authored.** All information lives in
  `library/entries/`.
- **Raw notes are immutable.** The agent reads them but never edits them.
- **Blank is better than invented.** If a field can't be determined, it is left empty
  and flagged in "Open Questions."
- **Every operation is logged.** `CHANGELOG.md` is the append-only audit trail.
- **Knowledge compounds.** Each ingested note improves future queries and pattern
  reports.
- **Consolidation is the point.** The primary value is identifying efforts that could
  share tooling, patterns, or infrastructure.

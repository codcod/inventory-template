# Opportunities

## Purpose

Compare the current entry landscape against the lifecycle model to identify stages
and activities that are not yet covered. This is the primary tool for strategic gap
analysis.

______________________________________________________________________

## When to use

- When someone asks "what are we missing?" or "where should we invest next?"
- Before a planning cycle or quarterly review.
- After a large batch of entries has been ingested.
- Before a new team or domain onboards, to identify the highest-value gaps to address
  first.

______________________________________________________________________

## Step-by-step instructions

### 1. Load the lifecycle reference

Read `agent/context/product-delivery-lifecycle.md` in full. Build a working model of
every stage: its slug, name, activities, roles, and artefacts.

### 2. Load the entry landscape

Read `MANIFEST.md` for the full list. Then open each `library/entries/<id>.md` to read:

- `lifecycle_stage` — which stage(s) it targets
- `category` and `problem` — what it does
- `status` and `Outcomes & Evidence` — activity level and maturity

If more than half the entry records have a blank `lifecycle_stage`, warn that coverage
mapping will be unreliable and recommend running `/v-ingest` to back-fill before
proceeding.

### 3. Map coverage

For each lifecycle stage, classify coverage as:

- **Strong** — two or more entries that are `status: active` AND have documented
  outcomes.
- **Emerging** — one active entry, OR multiple entries but none with measured
  outcomes.
- **Absent** — no entries targeting this stage at all.

Treat `status: proposed` entries as evidence of intent, not evidence of coverage.

### 4. Generate opportunity candidates

For each **Absent** or **Emerging** stage:

1. List the stage's activities from `agent/context/product-delivery-lifecycle.md`.
1. For each activity, assess whether a new entry could plausibly add value — name the
   activity specifically (not just the stage name).
1. Check whether any existing entry partially addresses this activity even if not
   tagged to this stage. If so, note it as a potential extension, not new work.
1. Rate each opportunity:
   - **Reach** — how many people would benefit? (individual, team, organization-wide)
   - **Feasibility** — can it be done with tooling and skills available today? (high,
     medium, low)
   - **Proximity** — is this close to something a team already does, making adoption
     easier? (high, medium, low)

### 5. Structure the report

Save to `library/outputs/opportunities-YYYY-MM-DD.md`:

```
# Opportunity Report
Generated: YYYY-MM-DD · Entries analysed: N · Lifecycle stages: N

## Coverage summary

| Stage | Slug | Coverage | Active entries |
| ----- | ---- | -------- | -------------- |
| ...one row per lifecycle stage... | | | <ids or none> |

## Strong coverage — no action needed
[List stages and the entries providing that coverage]

## Emerging coverage — worth monitoring
[For each: which entry exists, what gap remains, what would move it to Strong]

## Absent stages — highest opportunity
[For each: specific activities from the lifecycle file, rated by Reach / Feasibility /
Proximity. Note whether any existing entry could be extended rather than starting
fresh.]

## Recommended next entries
[3–5 specific ideas: name, target stage, problem statement, suggested approach, why now]

## Caveats
[What the inventory cannot see: un-ingested entries, informal work, incomplete
lifecycle documentation]
```

### 6. Append to CHANGELOG.md

Append a log entry for the `/s-opportunities` run: date, entries analysed, stages
covered, stages absent, and the top recommendations.

### 7. Epistemic discipline

- Distinguish "no entry captured in this inventory" from "definitely not happening."
  Teams may be doing things not yet ingested.
- Do not recommend entries that duplicate something already active.
- Prefer extensions of existing entries over net-new work where the extension is
  natural and the team already has the context.
- Separate confirmed coverage from probable coverage; use language like "likely
  covered — confirm with owner" for uncertain cases.

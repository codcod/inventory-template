# /s-opportunities

Compare the entry landscape against the lifecycle model and surface stages with no or
thin coverage as concrete, rated opportunity candidates.

## Instructions

Follow the workflow in `agent/prompts/opportunities_prompt.md`.

1. Read `agent/context/product-delivery-lifecycle.md` to load the lifecycle reference.
1. Read `MANIFEST.md` and all `library/entries/*.md` files to map coverage by stage
   using the `lifecycle_stage` frontmatter field.
1. Classify each lifecycle stage as **Strong**, **Emerging**, or **Absent** based on
   the number and maturity of active entries targeting it.
1. For Absent and Emerging stages, list the stage's specific activities from the
   lifecycle context file and generate opportunity candidates rated on Reach,
   Feasibility, and Proximity.
1. Save the report to `library/outputs/opportunities-YYYY-MM-DD.md` and print a
   summary.
1. Append an entry to `CHANGELOG.md`.

## Constraints

- Read-only on `library/raw/`, `library/entries/`, `agent/context/`, and
  `MANIFEST.md`.
- Do not create entry records — this command analyses; it does not ingest.
- If `lifecycle_stage` is blank on more than half the entry records, warn that
  coverage mapping is unreliable and recommend running `/v-ingest` to back-fill before
  interpreting the report.
- Never claim an activity is definitely uncovered; distinguish "not in inventory" from
  "definitely not happening."

## See also

- `agent/prompts/opportunities_prompt.md` — full step-by-step workflow
- `agent/context/product-delivery-lifecycle.md` — lifecycle reference
- `/v-ingest` — run first to ensure `lifecycle_stage` is populated on all records
- `/s-patterns` — complementary view: overlaps and consolidation within the existing
  landscape

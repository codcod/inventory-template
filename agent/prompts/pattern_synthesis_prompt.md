# Pattern Synthesis

## Purpose

Read all entry records in `library/entries/` and surface cross-cutting patterns:
duplicated effort, shared tooling opportunities, coverage gaps, stalled entries, and
consolidation candidates. This workflow produces a synthesis report for the
inventory's readers — not a manifest update.

______________________________________________________________________

## When to use

- Weekly or after a batch of new entries has been ingested.
- Before a planning cycle, to identify consolidation opportunities.
- When someone asks "what's happening across teams?"

______________________________________________________________________

## Step-by-step instructions

### 1. Read all entry records

Open every file in `library/entries/` (skip `.gitkeep`). Read both frontmatter and
body. Build a working model of each entry including: id, name, owner, team, status,
category, problem statement, tags, and outcomes.

### 2. Detect patterns

Apply each detection rule below. For each finding, note the confidence level:

- **Confirmed**: two or more signals clearly align.
- **Suspected**: one strong signal; needs owner confirmation.

#### Shared tags

Two or more entries in the same category sharing a tag (tool, platform, dependency).
These are candidates for a shared integration, shared library, or shared evaluation
approach.

Signal: `category` matches AND at least one `tags` entry matches.

#### Duplicate problems

Two or more entries addressing the same underlying pain with different approaches.
These are consolidation candidates — pick the best approach or merge.

Signal: `problem` statements are semantically similar AND `category` matches.

#### Stalled entries

Entries with `status: active` where `date_updated` is more than 90 days ago AND the
`Outcomes & Evidence` section is empty or contains only placeholder text. These may be
stalled and should be reviewed or closed.

#### Coverage gaps

Categories with only one entry vs. categories with four or more. A single entry may
indicate under-exploration; many entries in one category may indicate fragmentation.

#### Cross-team reuse potential

An entry in one team that solves a problem that appears in the "Open Questions" or
"Problem & Motivation" sections of an entry in a different team.

### 3. Structure the report

Save to `library/outputs/patterns-YYYY-MM-DD.md`:

```markdown
# Pattern Report

Generated: YYYY-MM-DD · Entries analyzed: N

## Consolidation Candidates

[For each candidate: name the entries, describe the overlap, and state a recommended
action. Distinguish confirmed from suspected overlaps.]

## Shared Tooling Opportunities

[List tag + the entries using it + what could be shared.]

## Stalled Entries

[List stalled entries with last-updated date and recommended action: escalate, close,
or re-confirm still active.]

## Coverage Gaps

[Categories with very few entries; categories that may be fragmented.]

## Cross-team Reuse

[Entries in different teams that could share components or learnings.]

## Summary

[Three to five bullet points: the most important findings.]
```

### 4. Tone and epistemic discipline

- Separate confirmed findings from suspected ones. Use language like "likely overlap —
  confirm with owners" for uncertain cases.
- Do not recommend organizational changes (team merges, reorgs) based on this data
  alone.
- Prefer concrete, named recommendations over vague "consider consolidating."
- If the data is too sparse to draw conclusions in a section, say so rather than
  filling it with weak observations.

______________________________________________________________________

## Constraints

- This workflow is read-only. Do not edit entry files or `MANIFEST.md`.
- Do not treat the report as a manifest update — it is a synthesis document for human
  review.
- If fewer than three entries exist, note that patterns are not yet detectable and
  recommend ingesting more data before running this workflow.

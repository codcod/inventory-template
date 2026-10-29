# /s-patterns

Read all entry records in `library/entries/` and produce a pattern synthesis report
surfacing overlaps, consolidation candidates, stalled entries, and coverage gaps.

## Instructions

Follow the workflow documented in `agent/prompts/pattern_synthesis_prompt.md` exactly.

Key detection rules:

- **Shared tags**: same category + overlapping tags → shared tooling opportunity.
- **Duplicate problems**: semantically similar problem statements in the same
  category → consolidation candidate.
- **Stalled entries**: `status: active`, `date_updated` > 90 days ago, no outcomes
  documented → flag for review.
- **Coverage gaps**: categories with one entry (under-explored) or five or more
  (possibly fragmented).
- **Cross-team reuse**: problems stated in one team's entry appearing in another
  team's open questions.

## Output format

Produce a structured report with sections: Consolidation Candidates, Shared Tooling
Opportunities, Stalled Entries, Coverage Gaps, Cross-team Reuse, Summary.

Distinguish confirmed findings from suspected ones. Recommend concrete actions, not
vague "consider consolidating."

## Constraints

- Read-only — do not modify entry files or `MANIFEST.md`.
- If fewer than three entries exist, state that patterns are not yet detectable.

## See also

- `agent/prompts/pattern_synthesis_prompt.md` — full detection rules and report
  structure

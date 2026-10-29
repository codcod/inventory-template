#!/usr/bin/env bash
# tools/clean-all.sh
#
# Restore the inventory to a clean starting point by removing all agent-generated
# files. After running this, execute /v-ingest in Claude Code to regenerate the
# inventory from the current library/raw/ notes.
#
# What is removed:
#   library/entries/*.md     — generated entry records       (.gitkeep preserved)
#   library/outputs/*.md      — dated reports                 (.gitkeep preserved)
#   MANIFEST.md               — reset to empty-table state
#   CHANGELOG.md              — reset to header only, with a clean-all entry appended
#
# What is kept (untouched):
#   library/raw/      — immutable source notes
#   agent/context/    — lifecycle reference
#   agent/templates/  — entry template (agent-internal)
#   library/templates/— input templates for contributors
#   agent/prompts/    — workflow prompts
#   .claude/commands/ — slash commands
#   CLAUDE.md, README.md, .github/, .editorconfig, .mcp.json, justfile

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TODAY="$(date +%Y-%m-%d)"
removed_entries=0
removed_outputs=0

echo "inventory clean-all"
echo "Root: $REPO_ROOT"
echo ""

# ── Entry records ────────────────────────────────────────────────────────────

echo "entries/"
while IFS= read -r -d '' f; do
    rm "$f"
    echo "  removed: $(basename "$f")"
    removed_entries=$((removed_entries + 1))
done < <(find "$REPO_ROOT/library/entries" -maxdepth 1 -name "*.md" -print0 2>/dev/null)
[ "$removed_entries" -eq 0 ] && echo "  (nothing to remove)"

# ── Output reports ────────────────────────────────────────────────────────────

echo "outputs/"
while IFS= read -r -d '' f; do
    rm "$f"
    echo "  removed: $(basename "$f")"
    removed_outputs=$((removed_outputs + 1))
done < <(find "$REPO_ROOT/library/outputs" -maxdepth 1 -name "*.md" -print0 2>/dev/null)
[ "$removed_outputs" -eq 0 ] && echo "  (nothing to remove)"

# ── Reset MANIFEST.md ─────────────────────────────────────────────────────────

cat >"$REPO_ROOT/MANIFEST.md" <<'MANIFEST_EOF'
# Inventory Manifest

> Single source of truth for all entries in the inventory. Regenerated from
> `library/entries/*.md` frontmatter. Do not edit rows by hand — update the underlying
> entry file and re-run `/v-ingest` or `/v-manifest-sync`.

Last updated: — · Total entries: 0

| ID | Entry | Owner | Team | Status | Category | Updated | Detail |
| -- | ----- | ----- | ---- | ------ | -------- | ------- | ------ |

## Summary by category

(none — run `/v-ingest` to populate)

## Notes

- Flag duplicates, overlaps, and consolidation candidates here as they emerge.
MANIFEST_EOF

echo "MANIFEST.md  reset"

# ── Reset CHANGELOG.md ──────────────────────────────────────────────────────────────

# Static header written with a quoted heredoc so backtick fences are literal.
cat >"$REPO_ROOT/CHANGELOG.md" <<'LOG_EOF'
# Operation Log

Append-only chronological record of every operation that changes the wiki: ingests,
manual record edits synced to the manifest, lints, and notable findings. Newest entries
at the bottom. Never rewrite or delete past entries — this is the audit trail.

Each entry follows:

```
## YYYY-MM-DD — <operation>

- Scope: <what was processed>
- Created: <entry ids>
- Updated: <entry ids>
- Findings: <contradictions, overlaps, blanks, questions>
```

______________________________________________________________________
LOG_EOF

# Dynamic clean-all entry appended with an unquoted heredoc for variable expansion.
cat >>"$REPO_ROOT/CHANGELOG.md" <<LOG_ENTRY

## ${TODAY} — clean-all

- Scope: full repository reset via \`tools/clean-all.sh\`.
- Removed: ${removed_entries} entry record(s), ${removed_outputs} output report(s).
- MANIFEST.md reset to empty state.
- Next step: run \`/v-ingest\` in Claude Code to regenerate all records from \`library/raw/\`.
LOG_ENTRY

echo "CHANGELOG.md       reset"
echo ""
echo "Done. Run /v-ingest to regenerate the inventory from library/raw/."

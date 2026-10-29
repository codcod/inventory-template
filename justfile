# https://just.systems

# List available targets (default)
default:
    just --list

# Restore the repository to a clean starting point — removes all agent-generated files
# (entry records, output reports, manifest rows, log). Run /v-ingest afterwards
# to regenerate the inventory from library/raw/.
clean-all:
    bash tools/clean-all.sh

# Generate a PDF report of entries grouped by lifecycle stage and status.
pdf:
    .venv/bin/python3 tools/generate_pdf.py

# Format all markdown files to 88-character line width.
# Excludes library/entries/, agent/context/ and both templates/ dirs — those files contain YAML
# frontmatter that mdformat corrupts without the mdformat-frontmatter plugin installed.
fmt:
    find . -name "*.md" \
        -not -path "./.git/*" \
        -not -path "./library/entries/*" \
        -not -path "./agent/templates/*" \
        -not -path "./agent/context/*" \
        -not -path "./library/templates/*" \
        | xargs mdformat --wrap 88

# vim: set ft=make:et:ai:

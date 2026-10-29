#!/usr/bin/env python3
"""Generate a PDF report of inventory entries grouped by lifecycle stage and status."""

import re
import subprocess
import sys
import typing as tp
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
ENTRIES_DIR = REPO_ROOT / "library" / "entries"
OUTPUTS_DIR = REPO_ROOT / "library" / "outputs"

TODAY = date.today().isoformat()

# Keep in sync with agent/context/product-delivery-lifecycle.md.
PHASE_ORDER: tp.List[str] = [
    "idea",
    "discovery",
    "ideation",
    "development-and-delivery",
    "gtm",
]
PHASE_LABELS: tp.Dict[str, str] = {
    "idea": "Idea",
    "discovery": "Discovery",
    "ideation": "Ideation",
    "development-and-delivery": "Development & Delivery",
    "gtm": "GTM",
}
PHASE_DESCRIPTIONS: tp.Dict[str, str] = {
    "idea": (
        "Capture and triage concepts worth exploring; qualify them against "
        "strategic goals before committing to discovery work."
    ),
    "discovery": (
        "Understand the problem before committing to a solution; test risky assumptions "
        "and produce enough clarity to decide confidently whether and how to proceed."
    ),
    "ideation": (
        "Shape potential solutions from the validated problem; design and test concepts; "
        "produce a clear solution direction and a ready story backlog."
    ),
    "development-and-delivery": (
        "Build and validate the solution in iterative sprints, delivering incremental "
        "releasable value; every change carries its own evidence of correctness."
    ),
    "gtm": (
        "Release into production; coordinate go-to-market; confirm monitoring; "
        "measure outcomes; and retire features that no longer serve users."
    ),
}

# Keep in sync with the status values in agent/templates/entry_template.md.
STATUS_ORDER: tp.List[str] = ["active", "proposed", "paused", "completed", "abandoned"]
STATUS_LABELS: tp.Dict[str, str] = {
    "active": "Active",
    "proposed": "Proposed",
    "paused": "Paused",
    "completed": "Completed",
    "abandoned": "Abandoned",
    "unknown": "Status unknown",
}

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

Frontmatter = tp.Dict[str, tp.Any]
Entry = tp.Tuple[Frontmatter, str]
PhaseGroup = tp.Dict[str, tp.List[Entry]]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_frontmatter(path: Path) -> tp.Tuple[Frontmatter, str]:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not match:
        return {}, content
    fm: Frontmatter = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).strip()
    return fm, body


# ---------------------------------------------------------------------------
# Body extraction helpers
# ---------------------------------------------------------------------------


def extract_section(body: str, section_name: str, max_bullets: int = 3) -> tp.List[str]:
    """Extract up to max_bullets bullet points from a named ## section."""
    pattern = rf"^##\s+{re.escape(section_name)}\s*\n(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, body, re.MULTILINE | re.DOTALL)
    if not match:
        return []
    bullets: tp.List[str] = []
    for line in match.group(1).split("\n"):
        line = line.strip()
        if line.startswith(("- ", "* ")):
            bullet = line[2:].strip()
            bullet = re.sub(r"\[\[([^\]]+)\]\]", r"\1", bullet)
            bullets.append(bullet)
            if len(bullets) >= max_bullets:
                break
    return bullets


def extract_summary(body: str) -> str:
    """Extract and truncate the Summary section to two sentences."""
    pattern = r"^##\s+Summary\s*\n(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, body, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    first_para = match.group(1).strip().split("\n\n")[0].strip()
    sentences = re.split(r"(?<=[.!?])\s+", first_para)
    return " ".join(sentences[:2])


# ---------------------------------------------------------------------------
# Frontmatter field helpers
# ---------------------------------------------------------------------------


def get_primary_phase(fm: Frontmatter) -> str:
    lifecycle = fm.get("lifecycle_stage")
    if isinstance(lifecycle, list) and lifecycle:
        return str(lifecycle[0]).strip()
    if isinstance(lifecycle, str) and lifecycle.strip():
        return lifecycle.strip()
    return "uncategorised"


def normalise_status(fm: Frontmatter) -> str:
    status = str(fm.get("status") or "").lower()
    return status if status in STATUS_ORDER else "unknown"


def format_list(value: tp.Any) -> str:
    if not value:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def format_related(related: tp.Any) -> str:
    if not related:
        return ""
    ids: tp.List[str] = []
    for r in related if isinstance(related, list) else [related]:
        m = re.search(r"\[\[([^\]]+)\]\]", str(r))
        ids.append(m.group(1) if m else str(r))
    return ", ".join(ids)


def format_links(links: tp.Any) -> str:
    """Render one or more URLs as comma-separated Markdown links."""
    if not links:
        return ""
    items = links if isinstance(links, list) else [links]
    rendered: tp.List[str] = []
    for item in items:
        url = str(item).strip()
        if not url:
            continue
        rendered.append(f"[{url}]({url})")
    return ", ".join(rendered)


# ---------------------------------------------------------------------------
# Card rendering
# ---------------------------------------------------------------------------


def render_card(fm: Frontmatter, body: str) -> str:
    name = fm.get("name") or fm.get("id") or "Unknown"
    team = fm.get("team") or "—"
    owner = fm.get("owner") or "—"
    status = (fm.get("status") or "—").capitalize()
    category = fm.get("category") or "—"
    tags = format_list(fm.get("tags"))
    problem = fm.get("problem") or ""
    lifecycle_str = format_list(fm.get("lifecycle_stage"))
    related = format_related(fm.get("related"))
    docs = format_links(fm.get("docs"))
    source = format_links(fm.get("source"))

    summary = extract_summary(body)
    approach = extract_section(body, "Approach", max_bullets=3)
    current_state = extract_section(body, "Current State", max_bullets=2)
    outcomes = extract_section(body, "Outcomes & Evidence", max_bullets=2)

    out: tp.List[str] = [f"### {name}\n"]
    out.append("| | |")
    out.append("|:--|:--|")
    out.append(f"| **Team** | {team} |")
    out.append(f"| **Contact** | {owner} |")
    out.append(f"| **Status** | {status} |")
    out.append(f"| **Category** | {category} |")
    if tags:
        out.append(f"| **Tags** | {tags} |")
    if lifecycle_str:
        out.append(f"| **Lifecycle stage(s)** | {lifecycle_str} |")
    if docs:
        out.append(f"| **Docs** | {docs} |")
    if source:
        out.append(f"| **Source** | {source} |")
    out.append("")

    if problem:
        out.append(f"**Problem:** {problem}\n")
    if summary:
        out.append(f"**What it does:** {summary}\n")
    if approach:
        out.append("**Approach:**")
        out.extend(f"- {b}" for b in approach)
        out.append("")
    if current_state:
        out.append("**Where it is now:**")
        out.extend(f"- {b}" for b in current_state)
        out.append("")
    if outcomes:
        out.append("**Evidence:**")
        out.extend(f"- {b}" for b in outcomes)
        out.append("")
    if related:
        out.append(f"**Related entries:** {related}\n")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Opportunities report helper
# ---------------------------------------------------------------------------


def extract_opportunities(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    match = re.search(
        r"^## Recommended next entries\s*\n(.*?)(?=^## Caveats|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def find_latest_opportunities() -> tp.Optional[Path]:
    reports = sorted(OUTPUTS_DIR.glob("opportunities-*.md"))
    return reports[-1] if reports else None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    entries: tp.List[Entry] = []
    for path in sorted(ENTRIES_DIR.glob("*.md")):
        if path.name.startswith("."):
            continue
        fm, body = parse_frontmatter(path)
        if not fm or not fm.get("id"):
            continue
        entries.append((fm, body))

    if not entries:
        print("No entries found.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(entries)} entries.")

    # Group: phase → status → [Entry]
    groups: tp.Dict[str, PhaseGroup] = {p: {} for p in PHASE_ORDER}
    uncategorised: PhaseGroup = {}

    for fm, body in entries:
        phase = get_primary_phase(fm)
        status = normalise_status(fm)
        target: PhaseGroup = groups[phase] if phase in groups else uncategorised
        target.setdefault(status, []).append((fm, body))
        if phase not in groups:
            print(
                f"  Warning: unknown phase '{phase}' for '{fm.get('id')}'"
                " — placing in Uncategorised",
                file=sys.stderr,
            )

    status_order = STATUS_ORDER + ["unknown"]

    # Build markdown
    lines: tp.List[str] = []

    lines += [
        "---",
        'title: "Inventory"',
        f'subtitle: "Inventory landscape — {TODAY}"',
        f"date: {TODAY}",
        "toc: true",
        "toc-depth: 3",
        'geometry: "margin=2.5cm, top=3cm, bottom=3cm"',
        "fontsize: 10pt",
        "colorlinks: true",
        "linkcolor: NavyBlue",
        "urlcolor: NavyBlue",
        "numbersections: true",
        "---",
        "",
    ]

    total = len(entries)
    lines += [
        "# About this document {.unnumbered}",
        "",
        (
            "This document maps every entry in the inventory. "
            "Entries are grouped by where they sit in the lifecycle, then by status. "
            "Each card shows the problem being solved, the approach, current state, "
            "and who to contact."
        ),
        "",
        (
            f"**{total} entries** are documented. "
            "To propose a correction or add an entry, drop a note in `library/raw/`."
        ),
        "",
        "\\newpage",
        "",
    ]

    for phase in PHASE_ORDER:
        phase_entries = groups.get(phase, {})
        total_in_phase = sum(len(v) for v in phase_entries.values())
        if total_in_phase == 0:
            continue

        label = PHASE_LABELS[phase]
        desc = PHASE_DESCRIPTIONS[phase]
        count_str = f"{total_in_phase} entr{'ies' if total_in_phase != 1 else 'y'}"

        lines += [
            f"# {label}",
            "",
            f"*{desc}*",
            "",
            f"**{count_str} at this stage.**",
            "",
        ]

        for status in status_order:
            status_entries = phase_entries.get(status, [])
            if not status_entries:
                continue
            lines += [f"## {STATUS_LABELS[status]}", ""]
            for fm, body in sorted(status_entries, key=lambda x: x[0].get("name", "")):
                lines.append(render_card(fm, body))
                lines += ["---", ""]

    if uncategorised:
        lines += [
            "# Uncategorised",
            "",
            "*These entries could not be mapped to a lifecycle stage.*",
            "",
        ]
        for status in status_order:
            for fm, body in uncategorised.get(status, []):
                lines.append(render_card(fm, body))
                lines += ["---", ""]

    opp_path = find_latest_opportunities()
    if opp_path:
        opp_content = extract_opportunities(opp_path)
        if opp_content:
            lines += [
                "\\newpage",
                "",
                "# Identified Opportunities {.unnumbered}",
                "",
                (
                    "The following opportunities were identified by analysing gaps in the "
                    "current entry landscape against the full lifecycle."
                ),
                "",
                opp_content,
            ]
    else:
        print(
            "  Warning: no opportunities report found; section omitted.",
            file=sys.stderr,
        )

    output_md = OUTPUTS_DIR / f"inventory-{TODAY}.md"
    output_pdf = OUTPUTS_DIR / f"inventory-{TODAY}.pdf"

    output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote intermediate markdown: {output_md.name}")

    pandoc_cmd: tp.List[str] = [
        "pandoc",
        str(output_md),
        "-o",
        str(output_pdf),
        "--pdf-engine=xelatex",
        "-V",
        "mainfont=Georgia",
        "-V",
        "monofont=Menlo",
    ]

    print("Running pandoc...")
    result = subprocess.run(pandoc_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"pandoc failed:\n{result.stderr}", file=sys.stderr)
        print(f"Intermediate markdown preserved at: {output_md}", file=sys.stderr)
        sys.exit(1)

    print(f"PDF written: {output_pdf.name}")


if __name__ == "__main__":
    main()

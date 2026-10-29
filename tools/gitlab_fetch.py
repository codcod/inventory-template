#!/usr/bin/env python3
"""Fetch GitLab project data via the REST API; write a note to library/raw/.

Usage (via /v-gitlab-fetch slash command):

    python3 tools/gitlab_fetch.py <project> [--gitlab-url <url>]

Writes a Markdown note to library/raw/.
"""

import argparse
import json
import os
import sys
import typing as tp
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).parent.parent
RAW_DIR = REPO_ROOT / "library" / "raw"

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

JsonDict = tp.Dict[str, tp.Any]
JsonList = tp.List[tp.Any]


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def _request(url: str, token: str) -> urllib.request.Request:
    """Build an authenticated GET request."""
    return urllib.request.Request(url, headers={"PRIVATE-TOKEN": token})


def fetch_json(url: str, token: str) -> tp.Any:
    """Fetch *url* and parse the JSON body. Exit 1 on any HTTP error."""
    req = _request(url, token)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code}: {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Request failed ({exc.reason}): {url}", file=sys.stderr)
        sys.exit(1)


def fetch_text(url: str, token: str) -> tp.Optional[str]:
    """Fetch *url* as plain text. Returns None on 404; exits 1 on other errors."""
    req = _request(url, token)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        print(f"HTTP {exc.code}: {url}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"Request failed ({exc.reason}): {url}", file=sys.stderr)
        sys.exit(1)



# ---------------------------------------------------------------------------
# GitLab API calls — metadata & content
# ---------------------------------------------------------------------------


def get_project(base_url: str, project_id: str, token: str) -> JsonDict:
    """GET /projects/:id — core project metadata."""
    url = f"{base_url}/api/v4/projects/{project_id}"
    result = fetch_json(url, token)
    if not isinstance(result, dict):
        print(f"Unexpected response from {url}", file=sys.stderr)
        sys.exit(1)
    return result


def get_languages(base_url: str, project_id: str, token: str) -> tp.Dict[str, float]:
    """GET /projects/:id/languages — language percentage breakdown."""
    url = f"{base_url}/api/v4/projects/{project_id}/languages"
    result = fetch_json(url, token)
    return {k: float(v) for k, v in result.items()} if isinstance(result, dict) else {}


def get_readme(
    base_url: str,
    project_id: str,
    ref: str,
    token: str,
    max_chars: int = 2000,
) -> str:
    """Try README.md, README.rst, readme.md; return up to *max_chars* or ''."""
    branch = quote(ref, safe="")
    for filename in ("README.md", "README.rst", "readme.md"):
        encoded = quote(filename, safe="")
        url = (
            f"{base_url}/api/v4/projects/{project_id}"
            f"/repository/files/{encoded}/raw?ref={branch}"
        )
        content = fetch_text(url, token)
        if content is not None:
            return content[:max_chars]
    return ""


def get_issues(base_url: str, project_id: str, token: str) -> JsonList:
    """GET /projects/:id/issues — up to 10 open issues."""
    url = f"{base_url}/api/v4/projects/{project_id}/issues?state=opened&per_page=10"
    result = fetch_json(url, token)
    return result if isinstance(result, list) else []


def get_merge_requests(base_url: str, project_id: str, token: str) -> JsonList:
    """GET /projects/:id/merge_requests — up to 10 open merge requests."""
    url = (
        f"{base_url}/api/v4/projects/{project_id}"
        "/merge_requests?state=opened&per_page=10"
    )
    result = fetch_json(url, token)
    return result if isinstance(result, list) else []


def get_pipelines(base_url: str, project_id: str, token: str) -> JsonList:
    """GET /projects/:id/pipelines — the 5 most recent pipelines."""
    url = f"{base_url}/api/v4/projects/{project_id}/pipelines?per_page=5"
    result = fetch_json(url, token)
    return result if isinstance(result, list) else []


def get_commits(base_url: str, project_id: str, token: str) -> JsonList:
    """GET /projects/:id/repository/commits — the 5 most recent commits."""
    url = f"{base_url}/api/v4/projects/{project_id}/repository/commits?per_page=5"
    result = fetch_json(url, token)
    return result if isinstance(result, list) else []


# ---------------------------------------------------------------------------
# Note rendering
# ---------------------------------------------------------------------------


def render_full_note(
    project: JsonDict,
    languages: tp.Dict[str, float],
    readme: str,
    issues: JsonList,
    mrs: JsonList,
    pipelines: JsonList,
    commits: JsonList,
) -> str:
    """Render a project summary note."""
    today = date.today().isoformat()
    name: str = project.get("name") or "Unknown"
    web_url: str = project.get("web_url") or ""
    visibility: str = project.get("visibility") or "\u2014"
    default_branch: str = project.get("default_branch") or "main"
    created = date_only(project.get("created_at") or "")
    last_activity = date_only(project.get("last_activity_at") or "")
    topics: tp.List[str] = project.get("topics") or []
    description = (project.get("description") or "").strip() or "No description."

    issues_body = "\n".join(format_issue(i) for i in issues) if issues else "None."
    mrs_body = "\n".join(format_mr(mr) for mr in mrs) if mrs else "None."
    pipelines_body = (
        "\n".join(format_pipeline(p) for p in pipelines) if pipelines else "None."
    )
    commits_body = "\n".join(format_commit(c) for c in commits) if commits else "None."

    lines: tp.List[str] = [
        f"# GitLab project: {name}",
        "",
        f"**URL:** {web_url}",
        f"**Fetched:** {today}",
        f"**Visibility:** {visibility}",
        f"**Default branch:** {default_branch}",
        f"**Created:** {created}",
        f"**Last activity:** {last_activity}",
        f"**Topics:** {format_topics(topics)}",
        f"**Top languages:** {format_top_languages(languages)}",
        "",
        "## Description",
        "",
        description,
        "",
        "## README (excerpt)",
        "",
        readme.strip() if readme else "No README found.",
        "",
        f"## Open issues ({len(issues)})",
        "",
        issues_body,
        "",
        f"## Open merge requests ({len(mrs)})",
        "",
        mrs_body,
        "",
        "## Recent pipelines",
        "",
        pipelines_body,
        "",
        "## Recent commits",
        "",
        commits_body,
        "",
        "## Notes for ingestion",
        "",
        (
            "Fetched automatically from GitLab. Verify owner, team, and"
            " entry details before ingesting."
        ),
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Shared formatting helpers
# ---------------------------------------------------------------------------


def date_only(iso: str) -> str:
    """Extract the YYYY-MM-DD portion from an ISO 8601 timestamp."""
    return iso[:10] if iso else "\u2014"


def format_topics(topics: tp.List[str]) -> str:
    """Comma-separated topic list, or '—' when empty."""
    return ", ".join(str(t) for t in topics) if topics else "\u2014"


def format_top_languages(langs: tp.Dict[str, float], n: int = 3) -> str:
    """Top *n* languages sorted by percentage, e.g. 'Python (45.2%)'."""
    top = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)
    parts = [f"{name} ({pct:.1f}%)" for name, pct in top[:n]]
    return ", ".join(parts) if parts else "\u2014"


def format_issue(issue: JsonDict) -> str:
    iid = issue.get("iid", "?")
    title = issue.get("title", "")
    labels: tp.List[str] = issue.get("labels") or []
    label_str = f" [{', '.join(labels)}]" if labels else ""
    return f"- #{iid} {title}{label_str}"


def format_mr(mr: JsonDict) -> str:
    iid = mr.get("iid", "?")
    title = mr.get("title", "")
    author = (mr.get("author") or {}).get("name", "unknown")
    created = date_only(mr.get("created_at") or "")
    return f"- !{iid} {title} \u2014 {author} ({created})"


def format_pipeline(pipeline: JsonDict) -> str:
    status = pipeline.get("status", "unknown")
    ref = pipeline.get("ref", "?")
    created = date_only(pipeline.get("created_at") or "")
    return f"- {status} on {ref} ({created})"


def format_commit(commit: JsonDict) -> str:
    short_id = commit.get("short_id", "?")
    title = commit.get("title", "")
    author = commit.get("author_name", "unknown")
    created = date_only(commit.get("created_at") or "")
    return f"- {short_id} {title} \u2014 {author} ({created})"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def encode_project_id(project_path_or_id: str) -> str:
    """Numeric IDs pass through; text slugs get / replaced with %2F."""
    if project_path_or_id.isdigit():
        return project_path_or_id
    return project_path_or_id.replace("/", "%2F")


def output_slug(project_path_or_id: str) -> str:
    """Derive a filesystem-safe slug for the output filename."""
    return project_path_or_id.replace("/", "-")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch a GitLab project and write a structured Markdown note"
            " to library/raw/."
        ),
    )
    parser.add_argument(
        "project",
        metavar="project-path-or-id",
        help=("GitLab project path (e.g. mygroup/myproject) or a numeric project ID."),
    )
    parser.add_argument(
        "--gitlab-url",
        default="https://gitlab.com",
        metavar="URL",
        help="GitLab base URL (default: https://gitlab.com).",
    )

    args = parser.parse_args()

    token = os.environ.get("GITLAB_TOKEN")
    if not token:
        print(
            "Error: GITLAB_TOKEN environment variable is not set.\n"
            "Export a GitLab personal access token with read_api scope:\n"
            "  export GITLAB_TOKEN=<your-token>",
            file=sys.stderr,
        )
        sys.exit(1)

    base_url: str = args.gitlab_url.rstrip("/")
    raw_input: str = args.project
    project_id = encode_project_id(raw_input)

    print(f"Fetching metadata for {raw_input!r} ...", file=sys.stderr)
    project = get_project(base_url, project_id, token)
    ref: str = project.get("default_branch") or "main"

    print("Fetching full repo summary ...", file=sys.stderr)
    languages = get_languages(base_url, project_id, token)
    print("  languages ... done", file=sys.stderr)
    readme = get_readme(base_url, project_id, ref, token)
    print(
        f"  README ({'found' if readme else 'not found'}) ... done", file=sys.stderr
    )
    issues = get_issues(base_url, project_id, token)
    print(f"  issues ({len(issues)}) ... done", file=sys.stderr)
    mrs = get_merge_requests(base_url, project_id, token)
    print(f"  merge requests ({len(mrs)}) ... done", file=sys.stderr)
    pipelines = get_pipelines(base_url, project_id, token)
    print(f"  pipelines ({len(pipelines)}) ... done", file=sys.stderr)
    commits = get_commits(base_url, project_id, token)
    print(f"  commits ({len(commits)}) ... done", file=sys.stderr)
    note = render_full_note(project, languages, readme, issues, mrs, pipelines, commits)

    today = date.today().isoformat()
    slug = output_slug(raw_input)
    filename = f"{today}_gitlab-{slug}.md"
    output_path = RAW_DIR / filename
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(note, encoding="utf-8")
    print(f"Written: library/raw/{filename}")


if __name__ == "__main__":
    main()

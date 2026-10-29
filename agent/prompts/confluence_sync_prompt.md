# Confluence Sync

## Purpose

Push the current inventory to a designated Confluence page. Writes a filtered table —
id, entry, owner, status, category — into an auto-managed section of the page without
touching any other content on that page.

______________________________________________________________________

## When to use

- After `/v-ingest` or `/v-manifest-sync`, when you want the Confluence page to
  reflect the latest inventory state.
- On demand via `/v-confluence-sync`.

______________________________________________________________________

## Inputs

- `MANIFEST.md` — source of truth for all rows and fields.
- `CLAUDE.md § Integrations` — contains the target Confluence page ID.

______________________________________________________________________

## Step-by-step instructions

### 1. Read the manifest

Read `MANIFEST.md`. Extract every data row from the entry table. For each row,
capture: id, entry (name), owner, status, category. Preserve the existing sort order
(category → name). Ignore all other columns.

### 2. Read the target page

Read `CLAUDE.md` to find the Confluence page ID under
`## Integrations → Confluence sync`. If it is still the `<CONFLUENCE_PAGE_ID>`
placeholder, stop and ask the user to set it.

Call `mcp__atlassian__getConfluencePage` with:

- `pageId`: the configured page ID
- `includeBody`: true

From the response, capture:

- `version.number` — required for the update call (Confluence rejects updates without
  the current version)
- The full page body (storage format)

If the call fails, stop immediately and report the error. Do not attempt to create a
new page.

### 3. Build the replacement section

Format the table as Confluence storage format (XHTML-compatible). Use this structure:

```xml
<h2>Inventory — auto-synced</h2>
<p><em>Last synced: YYYY-MM-DD · N entries · Source: MANIFEST.md</em></p>
<table>
  <tbody>
    <tr>
      <th>ID</th><th>Entry</th><th>Owner</th><th>Status</th><th>Category</th>
    </tr>
    <!-- one <tr> per entry row -->
    <tr>
      <td>001-example-entry</td>
      <td>Example Entry</td>
      <td>Jane Doe</td>
      <td>active</td>
      <td>category-a</td>
    </tr>
    <!-- ... -->
  </tbody>
</table>
```

Rules:

- Use today's date in the `Last synced` line.
- Leave blank `<td></td>` for any empty field — do not write "N/A" or similar.
- Do not link cells or add formatting beyond the table structure.
- Do not include the `Team`, `Updated`, or `Detail` columns.

### 4. Merge the section into the page body

Check whether the current page body already contains the string
`Inventory — auto-synced`.

- **Yes** — locate the `<h2>Inventory — auto-synced</h2>` element and replace
  everything from that `<h2>` through the closing `</table>` (and the `<p>` subtitle
  immediately after the heading) with the new section built in step 3.
- **No** — append the new section to the end of the page body.

The rest of the page content must remain unchanged.

### 5. Update the Confluence page

Call `mcp__atlassian__updateConfluencePage` with:

- `pageId`: same page ID from step 2
- `title`: the existing page title (unchanged)
- `version`: `version.number + 1`
- `body`: the merged body from step 4
- `bodyFormat`: `storage`

If the call returns an error, report it verbatim and stop. Do not retry silently.

### 6. Append to CHANGELOG.md

Append a one-line dated entry:

```
## YYYY-MM-DD — confluence-sync

- Page ID: <page-id>
- Rows synced: N
```

______________________________________________________________________

## Output

- Confluence page updated at the configured page ID.
- One-line entry appended to `CHANGELOG.md`.
- Print a confirmation: `Confluence synced — YYYY-MM-DD · N entries · page <id>`

______________________________________________________________________

## Constraints

- Read-only on all local files except `CHANGELOG.md`.
- Never edit `library/raw/`, `library/entries/`, or `MANIFEST.md`.
- Never create a new Confluence page — only update the configured one.
- Never invent or transform data. Mirror MANIFEST.md exactly, reformatted for
  Confluence.
- If the page ID is missing from `CLAUDE.md`, stop and ask the user to add it before
  proceeding.

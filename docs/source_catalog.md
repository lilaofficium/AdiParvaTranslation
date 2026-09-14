# Source Catalog

This file documents every external source used by the ETL project. Add one section for each URL.

## Source Table

| ID | Name | URL | Type | Encoding | Local file | Parser | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `mahabharata-k-01-sa` | Mahabharata Adi Parva - Sanskrit Documents | https://sanskritdocuments.org/mirrors/mahabharata/mbhK/mahabharata-k-01-sa.html | HTML | UTF-8 | `data/input/mahabharata-k-01-sa.html` | HTML parser | Active |

## Source: `mahabharata-k-01-sa`

### Identity

- Name: Mahabharata Adi Parva - Sanskrit Documents
- URL: https://sanskritdocuments.org/mirrors/mahabharata/mbhK/mahabharata-k-01-sa.html
- Source type: HTML webpage
- HTTP method: GET
- Language: Sanskrit (`sa`)
- Encoding: UTF-8
- Expected content type: `text/html`
- Status: Active

### Storage

- Downloaded HTML: `data/input/mahabharata-k-01-sa.html`
- Generated database: `data/output/translations.db`
- Downloaded HTML and generated database are ignored by Git.
- Keep this catalog and `config/source_manifest.json` under version control.

### Expected content

- Edition: Kumbhaghonam Edition
- Work: Adi Parva
- Chapter range shown by the page: 001 through 260
- Record unit to decide during parsing: chapter or verse
- Source text selector: To be confirmed after inspecting the HTML structure
- Translation text selector: To be confirmed after inspecting the HTML structure
- Section/verse selector: To be confirmed after inspecting the HTML structure

### Request notes

- Use a browser-like `User-Agent`, `Accept`, and `Accept-Language` header.
- Use a request timeout.
- Check the HTTP status before saving the response.
- Save only a successful response.

## How to add another source

1. Add a new object to `config/source_manifest.json`.
2. Add one row to the Source Table above.
3. Add a detailed section using the same headings.
4. Set the local file path and parser name.
5. Record the HTML selectors or JSON field paths after inspecting the source.
6. Add or update the parser chain if the new source format differs.

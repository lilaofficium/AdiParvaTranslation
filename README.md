# AdiParvaTranslation

## Browser control

The project uses `api_reader.py` to download HTML and Playwright to control a
browser page when the page's JavaScript must run. `api_reader.py` is unchanged.

Install the Python dependencies and the Chromium browser once:

```powershell
pip install -r Requirements.txt
python -m playwright install chromium
```

Run the browser controller. It calls the configured URL first, then loads the
returned HTML into Playwright:

```powershell
python -m src.adiparva_translation.browser_controller
```

The `get_chapter_from_api()` function calls `read_from_api()`, loads the
returned HTML with `page.set_content()`, clicks the first chapter accordion,
and executes JavaScript with `page.evaluate()`. Set `headless=False` in code
when you want to watch the browser.

## Convert HTML to JSON

Convert every HTML file in `data/input`. Each file creates a JSON file with the
same base filename in `data/output`, including chapters, topics, verse
references, RSN values, and Sanskrit text:

```powershell
python -m src.adiparva_translation.html_to_json
```

Custom directories can be supplied with `--input-dir` and `--output-dir`.

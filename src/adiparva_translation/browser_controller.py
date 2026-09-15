import sys
import time
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from playwright.sync_api import Page, sync_playwright

if __package__:
    from .api_reader import load_source_config, read_from_api
    from .file_manager import save_html
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from adiparva_translation.api_reader import load_source_config, read_from_api
    from adiparva_translation.file_manager import save_html

 

def convert_link_text_to_english(text: str) -> str: 
    translations = {
        "आदिपर्व": "Adi Parva",
        "सभापर्व": "Sabha Parva",
        "वनपर्व": "Vana Parva",
        "विराटपर्व": "Virata Parva",
        "उद्योगपर्व": "Udyoga Parva",
        "भीष्मपर्व": "Bhishma Parva",
        "द्रोणपर्व": "Drona Parva",
        "कर्णपर्व": "Karna Parva",
        "शाल्यपर्व": "Shalya Parva",
        "सौप्तिकपर्व": "Sauptika Parva",
        "स्त्रीपर्व": "Stri Parva",
        "शान्तिपर्व": "Shanti Parva",
        "अनुशासनपर्व": "Anushasana Parva",
        "अश्वमेधिकपर्व": "Ashvamedhika Parva",
        "आश्रमवासिकपर्व": "Ashramavasika Parva",
        "मौसलपर्व": "Mausala Parva",
        "महाप्रस्थानिकपर्व": "Mahaprasthanika Parva",
        "स्वर्गारोहणपर्व": "Svargarohana Parva",
    }
    converted = text.strip()
    for source, target in translations.items():
        converted = converted.replace(source, target)
    return converted.replace(" ", "_")


source_config = load_source_config()
html = read_from_api(source_config["url"])

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.set_content(html)

    links = page.evaluate("""
    () => {
        const header = [...document.querySelectorAll(
            "#accordion-container .accordion-header"
        )].find(el => {
            const text = el.textContent.replace(/\\s+/g, " ").trim();
            return /utf-8/i.test(text) && /\\bHTML\\b/i.test(text);
        });

        if (!header) return [];

        header.click();

        return [...header.nextElementSibling.querySelectorAll("a")]
            .map(a => a.href)
            .filter((href, i, arr) => arr.indexOf(href) === i);
    }
    """)

    browser.close()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
output_folder = PROJECT_ROOT / source_config["local_file"]
output_folder = output_folder.parent

for link in links:
    response = read_from_api(link)
    file_name = Path(unquote(urlparse(link).path)).name
    if not file_name:
        continue

    save_html(
        output_folder,
        file_name,
        response,
        encoding=source_config.get("encoding", "utf-8"),
    )
    # print(link)


 
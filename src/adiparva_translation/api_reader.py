import requests
import json
from pathlib import Path 
from .file_manager import save_html

 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = PROJECT_ROOT / "config" / "source_manifest.json"


def load_source_config(manifest_path=MANIFEST_PATH): 
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    active_sources = [
        source for source in manifest["sources"] if source.get("status") == "active"
    ]
    if not active_sources:
        raise ValueError("No active source found in the source manifest.")
    return active_sources[0]


def read_from_api(url, parameters=None, headers=None):
    # print(f"Fetching data from API: {url}")
    request_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    if headers:
        request_headers.update(headers)

    try:
        response = requests.get(
            url,
            params=parameters,
            headers=request_headers,
            timeout=30,
        )
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.text  # Convert the response to text
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching data from API: {e}")
        return None


if __name__ == "__main__":
    source = load_source_config()
    response = read_from_api(source["url"])

    if response is not None:
        output_path = PROJECT_ROOT / source["local_file"]
        save_html(
            output_path.parent,
            output_path.name,
            response,
            encoding=source.get("encoding", "utf-8"),
        )
        # print(f"Saved HTML file to: {output_path}")
    else:
        # print("HTML file was not saved because the request failed.")
        pass


#
# 2. Define the API URL as a constant or receive it as a function argument.
#    Do not hard-code private API keys in this file. Read secrets from environment variables.
#
# 3. Create a function such as read_from_api(url, parameters=None, headers=None).
#    The function should:
#       - send a GET or POST request to the API;
#       - pass query parameters, request headers, and authentication when required;
#       - set a timeout so the program does not wait forever;
#       - check whether the response was successful;
#       - convert the response to JSON when the API returns JSON;
#       - return the received data to pipeline.py.
#
# 4. Handle expected failures clearly:
#       - connection or timeout errors;
#       - HTTP errors such as 401, 404, or 500;
#       - invalid JSON or an unexpected response format.
#    Raise a useful error or return an explicit failure result. Do not silently ignore errors.
#
# 5. Keep this file limited to fetching data.
#    Put HTML/API data conversion in parser.py and database writes in database.py.
#
# 6. If the API uses pagination, add a helper or loop here to request every page.
#    Return one combined collection to the pipeline.
#
# 7. If the API requires rate limiting or retries, implement those here rather than in the parser.
#
# 8. Add tests later in tests/test_api_reader.py using mocked API responses.
#    Tests should cover a successful response, an HTTP failure, a timeout, and invalid data.
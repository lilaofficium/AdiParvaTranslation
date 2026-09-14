# api_reader.py responsibilities
#
# 1. Import the HTTP client that the project will use, for example:
#       import requests
#    Add that package to requirements.txt if it is not part of Python's standard library.
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
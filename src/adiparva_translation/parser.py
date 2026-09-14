# parser.py responsibilities
#
# 1. Import the tools needed to read and convert the data received from
#    api_reader.py or html_reader.py.
#
# 2. Define a clear data structure for one translation record. It may contain:
#       - source_file or source_url;
#       - section, chapter, or verse number;
#       - original Sanskrit/source text;
#       - translated text;
#       - optional author, language, or metadata fields.
#
# 3. Create a parser function, for example:
#       parse_translation_data(data)
#    The function should receive raw API JSON or HTML and return a consistent
#    list of translation records.
#
# 4. For JSON/API data:
#       - identify the fields containing the source and translated text;
#       - read chapter, section, and verse identifiers;
#       - handle nested objects and lists;
#       - use safe access for optional fields;
#       - convert the API response into the project's record format.
#
# 5. For HTML data:
#       - locate the HTML elements containing each translation;
#       - extract source and translated text;
#       - remove surrounding whitespace;
#       - preserve meaningful text while ignoring navigation and layout elements.
#
# 6. Validate each record before returning it:
#       - source text must not be empty;
#       - translated text must not be empty;
#       - identifiers should use the expected type and format.
#
# 7. Decide how malformed records are handled:
#       - skip them and log the reason; or
#       - raise a clear error when the data is required.
#    Do not silently create incomplete database records.
#
# 8. Keep this file focused on parsing and validation.
#    Fetching belongs in api_reader.py or html_reader.py.
#    Database inserts belong in database.py.
#
# 9. Add tests later in tests/test_parser.py for:
#       - one valid API response;
#       - one valid HTML document;
#       - multiple translation records;
#       - missing source or translated text;
#       - empty or unexpected API responses.

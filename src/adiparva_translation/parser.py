from __future__ import annotations

import re
from html.parser import HTMLParser

_REFERENCE = re.compile(r"(?P<parva>\d+)-(?P<chapter>\d+)-(?P<verse>\d+)(?P<variant>x?)")
_RSN = re.compile(r"\((?P<rsn>\d+)\)")

def _clean_text(value: str) -> str:
	return re.sub(r"\s+", " ", value).strip()

class _ChapterParser(HTMLParser):
	def __init__(self) -> None:
		super().__init__(convert_charrefs=True)
		self.heading: list[str] = []
		self.section: list[str] = []
		self.topic: list[str] = []
		self.chapter_text: list[str] = []
		self._heading_depth = 0
		self._section_depth = 0
		self._topic_depth = 0
		self._text_depth = 0
		self._ignored_depth = 0

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		attributes = dict(attrs)
		classes = set((attributes.get("class") or "").split())
		if tag in {"h6", "h2"} and not self._text_depth:
			self._heading_depth += 1
		if tag == "h3" and not self._text_depth:
			self._section_depth += 1
		if "topic" in classes:
			self._topic_depth += 1
		if "text" in classes:
			self._text_depth += 1
		if "RSN" in classes:
			self._ignored_depth += 1

	def handle_endtag(self, tag: str) -> None:
		if tag in {"h6", "h2"} and self._heading_depth:
			self._heading_depth -= 1
		if tag == "h3" and self._section_depth:
			self._section_depth -= 1
		if tag == "span" and self._topic_depth:
			self._topic_depth -= 1
		if tag == "div" and self._text_depth:
			self._text_depth -= 1
		if tag == "span" and self._ignored_depth:
			self._ignored_depth -= 1

	def handle_data(self, data: str) -> None:
		if self._ignored_depth:
			return
		if self._heading_depth:
			self.heading.append(data)
		elif self._section_depth:
			self.section.append(data)
		elif self._topic_depth:
			self.topic.append(data)
		elif self._text_depth:
			self.chapter_text.append(data)

def _parse_verses(text: str) -> list[dict[str, object]]:
	verses: list[dict[str, object]] = []
	matches = list(_REFERENCE.finditer(text))
	for index, match in enumerate(matches):
		next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
		content = _clean_text(text[match.end():next_start])
		rsn_match = _RSN.search(content)
		if rsn_match:
			content = _clean_text(content[:rsn_match.start()] + content[rsn_match.end():])
			rsn = int(rsn_match.group("rsn"))
		else:
			rsn = None
		verses.append(
			{
				"reference": match.group(0),
				"verse_number": int(match.group("verse")),
				"variant": bool(match.group("variant")),
				"rsn": rsn,
				"text": content,
			}
		)
	return verses

def parse_mahabharata_html(html: str, source_file: str | None = None) -> dict[str, object]:
	"""Return edition, parva, chapter, topic, and verse details from one HTML file."""
	chapters = []
	chapter_blocks = re.split(r"(?=<h6\b[^>]*accordion-header)", html)
	for block in chapter_blocks:
		if "accordion-header" not in block:
			continue
		parser = _ChapterParser()
		parser.feed(block)
		heading = _clean_text("".join(parser.heading))
		section_text = _clean_text("".join(parser.section))
		topic_text = _clean_text("".join(parser.topic))
		chapter_match = re.search(r"अध्याय\S*\s+(\d+)", heading)
		chapter_title = re.search(r"\(([^॥]+)", section_text)
		topics = [
			_clean_text(topic)
			for topic in re.split(r"॥\s*\d+\s*॥", topic_text)
			if _clean_text(topic)
		]
		chapters.append(
			{
				"number": int(chapter_match.group(1)) if chapter_match else len(chapters) + 1,
				"title": chapter_title.group(1).strip() if chapter_title else None,
				"topics": topics,
				"verses": _parse_verses("".join(parser.chapter_text)),
			}
		)

	parva_match = re.search(r"<h2>\s*(\d+)\.\s*([^\s<]+)", html)

	return {
		"edition": {
			"name": "Kumbhaghonam Edition",
			"tradition": "Southern Recension",
			"language": "Sanskrit",
			"source_file": source_file,
			"source": "https://sanskritdocuments.org/mirrors/mahabharata/mbhK/mahabharata-k-01-sa.html",
		},
		"parva": {
			"number": int(parva_match.group(1)) if parva_match else 1,
			"name_sanskrit": parva_match.group(2) if parva_match else "आदिपर्व",
			"name_english": "Adi Parva",
		},
		"chapters": chapters,
	}
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

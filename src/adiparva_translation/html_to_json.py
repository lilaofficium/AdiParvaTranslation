"""Convert a downloaded Mahabharata HTML file to JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .parser import parse_mahabharata_html


def convert_html_to_json(input_path: Path, output_path: Path) -> Path:
	"""Read one HTML file, parse it, and write UTF-8 JSON with Sanskrit preserved."""
	data = parse_mahabharata_html(
		input_path.read_text(encoding="utf-8"),
		source_file=str(input_path),
	)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(
		json.dumps(data, ensure_ascii=False, indent=2) + "\n",
		encoding="utf-8",
	)
	return output_path


def convert_input_directory(input_dir: Path, output_dir: Path) -> list[Path]:
	"""Convert every HTML file in input_dir to a same-named JSON file."""
	output_paths = []
	for html_path in sorted(input_dir.glob("*.html")):
		json_path = output_dir / f"{html_path.stem}.json"
		output_paths.append(convert_html_to_json(html_path, json_path))
	return output_paths


def main() -> None:
	project_root = Path(__file__).resolve().parents[2]
	argument_parser = argparse.ArgumentParser(description=__doc__)
	argument_parser.add_argument(
		"--input-dir",
		type=Path,
		default=project_root / "data/input",
		help="Directory containing HTML files to convert.",
	)
	argument_parser.add_argument(
		"--output-dir",
		type=Path,
		default=project_root / "data/output",
		help="Directory where same-named JSON files will be written.",
	)
	arguments = argument_parser.parse_args()
	output_paths = convert_input_directory(arguments.input_dir, arguments.output_dir)
	for output_path in output_paths:
		print(f"Saved {output_path}")
	print(f"Converted {len(output_paths)} HTML files.")

if __name__ == "__main__":
	main()

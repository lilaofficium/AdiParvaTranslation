"""Helpers for saving HTML files."""

from pathlib import Path


def save_html(
    folder: str | Path,
    file_name: str,
    html: str,
    encoding: str = "utf-8",
) -> Path:
    """Save HTML content in a folder and return the saved file path."""
    file_path = Path(folder) / file_name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(html, encoding=encoding)
    return file_path

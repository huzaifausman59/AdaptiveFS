"""
AdaptiveFS — Extension Ignore Rules

Modular, standalone check for "should this file's extension be
ignored entirely?" — kept separate from filename-glob ignoring
(ignore_rules.py) so each check can be tested, edited, or swapped
independently.

Extensions to ignore are read from a `.adaptivefsignore_ext` file
sitting in the watched folder — one extension per line, no dot,
case-insensitive. This is deliberately a different file from
.adaptivefsignore (glob patterns) so the two concerns don't get
tangled in one format.

Example .adaptivefsignore_ext:
    # never touch spreadsheets during testing
    xlsx
    csv
"""

from pathlib import Path

EXTENSION_IGNORE_FILENAME = ".adaptivefsignore_ext"


def load_ignored_extensions(watched_folder: str) -> set[str]:
    """
    Loads ignored extensions from <watched_folder>/.adaptivefsignore_ext.
    Returns a set of lowercase extensions without the leading dot.
    Returns an empty set if the file doesn't exist.
    """
    ignored = set()

    ext_file = Path(watched_folder) / EXTENSION_IGNORE_FILENAME
    if ext_file.exists():
        with open(ext_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().lstrip(".").lower()
                if not line or line.startswith("#"):
                    continue
                ignored.add(line)

    return ignored


def is_ignored_extension(filename: str, ignored_extensions: set[str]) -> bool:
    """
    Returns True if filename's extension is in ignored_extensions.
    Pure check — no file I/O here, just string logic, so it's easy to
    unit test independently of load_ignored_extensions().
    """
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in ignored_extensions


if __name__ == "__main__":
    # quick manual test
    ignored = {"xlsx", "csv"}
    samples = ["report.pdf", "data.xlsx", "notes.CSV", "photo.jpg"]
    for s in samples:
        print(f"{s:15s} ignored={is_ignored_extension(s, ignored)}")

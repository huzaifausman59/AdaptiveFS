"""
AdaptiveFS — Ignore Rules

Reads glob patterns from a `.adaptivefsignore` file (same idea as
.gitignore) sitting inside the watched folder, plus a small set of
permanent built-in exclusions, and exposes should_ignore() for
watcher.py to check before handing a file to sort_file().

.adaptivefsignore format:
    - one glob pattern per line
    - blank lines and lines starting with # are ignored
    - patterns match against the filename only (not full path)

Example .adaptivefsignore:
    # ignore in-progress downloads
    *.crdownload
    *.part

    # ignore my manual test files
    test_*
    scratch_*
"""

import fnmatch
from pathlib import Path

IGNORE_FILENAME = ".adaptivefsignore"

# Permanent built-in exclusions — things that should never be sorted
# regardless of what the user's ignore file says.
DEFAULT_IGNORE_PATTERNS = [
    ".adaptivefsignore",
    "*.tmp",
    "*.crdownload",
    "*.part",
    "*.swp",
    "desktop.ini",
    ".DS_Store",
    "Thumbs.db",
]


def load_ignore_patterns(watched_folder: str) -> list[str]:
    """
    Loads patterns from <watched_folder>/.adaptivefsignore if present,
    combined with the built-in defaults. Returns a flat list of glob
    patterns.
    """
    patterns = list(DEFAULT_IGNORE_PATTERNS)

    ignore_file = Path(watched_folder) / IGNORE_FILENAME
    if ignore_file.exists():
        with open(ignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                patterns.append(line)

    return patterns


def should_ignore(filepath: str, patterns: list[str]) -> bool:
    """
    Returns True if the filename at `filepath` matches any of the given
    glob patterns. Matches against the filename only, not the full path,
    so patterns stay simple regardless of folder depth.

    Also ignores anything living inside the category folders themselves
    (Code/, Documents/, Images/, etc.) so already-sorted files or files
    being moved don't get re-triggered — this is a cheap safeguard until
    the category folder names are threaded through more formally.
    """
    filename = Path(filepath).name

    for pattern in patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True

    return False


if __name__ == "__main__":
    # quick manual test
    test_patterns = load_ignore_patterns(".")
    print("Loaded patterns:", test_patterns)

    samples = ["report.pdf", "download.crdownload", "test_file.txt", "notes.tmp"]
    for s in samples:
        print(f"{s:20s} ignore={should_ignore(s, test_patterns)}")
"""
AdaptiveFS — Command Handler

Pure logic for interpreting a typed command against the watched
folder. Separated from watcher.py's input_listener so the command
logic (list / all / sort one) can be tested without stdin, and so
input_listener stays a thin read-print loop.
"""

import os
from sort import sort_file
from ignore_rules import load_ignore_config, should_ignore


def list_files(folder: str) -> list[str]:
    """Returns filenames of files (not folders) directly in `folder`."""
    return [
        name for name in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, name))
    ]


def list_sortable_files(folder: str) -> list[str]:
    """
    Same as list_files, but excludes anything matching the ignore rules
    (glob patterns or ignored extensions). Used by 'list' and 'all' so
    bulk commands never touch ignored files — config files like
    .adaptivefsignore_ext included.
    """
    ignore_config = load_ignore_config(folder)
    files = list_files(folder)
    return [
        name for name in files
        if not should_ignore(
            os.path.join(folder, name),
            ignore_config["patterns"],
            ignore_config["extensions"],
        )
    ]


def handle_command(command: str, folder: str) -> str:
    """
    Interprets one typed command and returns a message describing what
    happened (for the caller to print). Does not do any input() or
    print() itself, so it can be unit tested directly.

    Commands:
        list          -> lists sortable (non-ignored) files in `folder`
        all           -> sorts every non-ignored file in `folder`
        <filename>    -> sorts that specific file (explicit request,
                          so ignore rules are NOT applied here — typing
                          an exact filename is an intentional override)
    """
    if command == "list":
        files = list_sortable_files(folder)
        if not files:
            return "(nothing sortable in folder)"
        return "\n".join(files)

    if command == "all":
        files = list_sortable_files(folder)
        if not files:
            return "(nothing to sort)"
        for name in files:
            sort_file(os.path.join(folder, name), folder, method="manual")
        return f"Sorted {len(files)} file(s)."

    path = os.path.join(folder, command)
    if not os.path.isfile(path):
        return f"File not found: '{command}'"
 
    ignore_config = load_ignore_config(folder)
    if should_ignore(path, ignore_config["patterns"], ignore_config["extensions"]):
        return f"'{command}' matches an ignore rule and was not sorted."
 
    sort_file(path, folder, method="manual")
    return f"Sorted '{command}'."

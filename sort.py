import os
import shutil
from file_categories import get_category
from logger import log_action


def resolve_destination(file_path: str, base_dir: str) -> str:
    """
    Decide where a file should end up, based on its category.
    Pure logic — no filesystem writes happen here.

    file_path : full path to the file being classified
    base_dir  : root folder being organized (category folders live here)

    Returns the full destination file path (folder + filename),
    without checking for collisions or creating anything.
    """
    filename = os.path.basename(file_path)
    category = get_category(filename)
    
    dest_dir = os.path.join(base_dir, category)
    return os.path.join(dest_dir, filename)


def avoid_collision(dest_path: str) -> str:
    """
    If dest_path already exists, append (1), (2), etc. until it's unique.
    Pure logic — only checks existence, doesn't move anything.
    """
    if not os.path.exists(dest_path):
        return dest_path

    dest_dir = os.path.dirname(dest_path)
    name, ext = os.path.splitext(os.path.basename(dest_path))
    counter = 1
    new_path = dest_path
    while os.path.exists(new_path):
        new_path = os.path.join(dest_dir, f"{name} ({counter}){ext}")
        counter += 1
    return new_path


def move_file(src_path: str, dest_path: str) -> str:
    """
    Move a file from src_path to dest_path, creating the destination
    folder if needed. No categorization logic here — just the move.

    Returns the final path the file was moved to.
    """
    if not os.path.isfile(src_path):
        return src_path  # nothing to do

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    shutil.move(src_path, dest_path)
    return dest_path


def sort_file(file_path: str, base_dir: str, method: str = "manual") -> str:
    """
    High-level convenience wrapper: resolve where the file goes,
    avoid overwriting anything, then move it.

    method : how this sort was triggered, e.g. "watcher" or "manual".
             Passed straight through to the actions log so every logged
             row records who/what initiated the move.
    """
    if not os.path.isfile(file_path):
        print(f"[SKIP] Not a file (missing or already moved): {file_path}")
        return file_path

    dest_path = resolve_destination(file_path, base_dir)

    if os.path.dirname(file_path) == os.path.dirname(dest_path):
        return file_path

    dest_path = avoid_collision(dest_path)
    final_path = move_file(file_path, dest_path)

    print(f"[SORTED] {os.path.basename(final_path)} -> {os.path.dirname(final_path)}/")
    log_action(original_path=file_path, destination=final_path, method=method)

    return final_path
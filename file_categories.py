"""
AdaptiveFS — Extension-to-Category Mapping

This is Layer 1's dispatch table: maps a raw file extension to a broad
category. Used as the fallback / entry point before content-based
classification (DistilBERT embedding, code-context inference, etc.) refines
the decision further.

Notes:
- Keys are lowercase, without the leading dot.
- Ambiguous types (json, csv, xml) default to DOCUMENTS here; override with
  project-context inference (see section 4.2) when a codebase is detected.
- Extensions not present in this map should fall through to the
  metadata-only classifier described in section 6 (Format Opacity).
"""

CATEGORY_CODE = "Code"
CATEGORY_DOCUMENTS = "Documents"
CATEGORY_IMAGES = "Images"
CATEGORY_VIDEOS = "Videos"
CATEGORY_TEMPORARY = "Temporary"
CATEGORY_AUDIO = "Audio"
CATEGORY_ARCHIVES = "Archives"
CATEGORY_APPLICATION = "Application"

EXTENSION_CATEGORY_MAP = {
    # --- Code ---
    "py": CATEGORY_CODE,
    "js": CATEGORY_CODE,
    "ts": CATEGORY_CODE,
    "jsx": CATEGORY_CODE,
    "tsx": CATEGORY_CODE,
    "java": CATEGORY_CODE,
    "c": CATEGORY_CODE,
    "cpp": CATEGORY_CODE,
    "h": CATEGORY_CODE,
    "hpp": CATEGORY_CODE,
    "cs": CATEGORY_CODE,
    "go": CATEGORY_CODE,
    "rs": CATEGORY_CODE,
    "rb": CATEGORY_CODE,
    "php": CATEGORY_CODE,
    "swift": CATEGORY_CODE,
    "kt": CATEGORY_CODE,
    "sh": CATEGORY_CODE,
    "bash": CATEGORY_CODE,
    "sql": CATEGORY_CODE,
    "html": CATEGORY_CODE,
    "css": CATEGORY_CODE,
    "scss": CATEGORY_CODE,
    "r": CATEGORY_CODE,
    "lua": CATEGORY_CODE,
    "pl": CATEGORY_CODE,
    "ipynb": CATEGORY_CODE,

    # --- Documents ---
    "pdf": CATEGORY_DOCUMENTS,
    "doc": CATEGORY_DOCUMENTS,
    "docx": CATEGORY_DOCUMENTS,
    "txt": CATEGORY_DOCUMENTS,
    "md": CATEGORY_DOCUMENTS,
    "rtf": CATEGORY_DOCUMENTS,
    "odt": CATEGORY_DOCUMENTS,
    "xls": CATEGORY_DOCUMENTS,
    "xlsx": CATEGORY_DOCUMENTS,
    "csv": CATEGORY_DOCUMENTS,       # override to Code if project-context detected
    "ppt": CATEGORY_DOCUMENTS,
    "pptx": CATEGORY_DOCUMENTS,
    "epub": CATEGORY_DOCUMENTS,
    "mobi": CATEGORY_DOCUMENTS,
    "json": CATEGORY_DOCUMENTS,      # override to Code if project-context detected
    "xml": CATEGORY_DOCUMENTS,       # override to Code if project-context detected
    "yaml": CATEGORY_DOCUMENTS,      # override to Code if project-context detected
    "yml": CATEGORY_DOCUMENTS,       # override to Code if project-context detected

    # --- Images ---
    "jpg": CATEGORY_IMAGES,
    "jpeg": CATEGORY_IMAGES,
    "png": CATEGORY_IMAGES,
    "gif": CATEGORY_IMAGES,
    "bmp": CATEGORY_IMAGES,
    "webp": CATEGORY_IMAGES,
    "svg": CATEGORY_IMAGES,
    "tiff": CATEGORY_IMAGES,
    "heic": CATEGORY_IMAGES,
    "raw": CATEGORY_IMAGES,
    "psd": CATEGORY_IMAGES,          # design file, flagged as judgment call
    "ai": CATEGORY_IMAGES,           # design file, flagged as judgment call
    "sketch": CATEGORY_IMAGES,       # design file, flagged as judgment call
    "fig": CATEGORY_IMAGES,          # design file, flagged as judgment call

    # --- Videos ---
    "mp4": CATEGORY_VIDEOS,
    "mkv": CATEGORY_VIDEOS,
    "avi": CATEGORY_VIDEOS,
    "mov": CATEGORY_VIDEOS,
    "wmv": CATEGORY_VIDEOS,
    "flv": CATEGORY_VIDEOS,
    "webm": CATEGORY_VIDEOS,
    "m4v": CATEGORY_VIDEOS,

    # --- Temporary ---
    "tmp": CATEGORY_TEMPORARY,
    "temp": CATEGORY_TEMPORARY,
    "bak": CATEGORY_TEMPORARY,
    "crdownload": CATEGORY_TEMPORARY,
    "part": CATEGORY_TEMPORARY,
    "swp": CATEGORY_TEMPORARY,
    "~": CATEGORY_TEMPORARY,
    "log": CATEGORY_TEMPORARY,

    # --- Audio ---
    "mp3": CATEGORY_AUDIO,
    "wav": CATEGORY_AUDIO,
    "flac": CATEGORY_AUDIO,
    "aac": CATEGORY_AUDIO,
    "ogg": CATEGORY_AUDIO,
    "wma": CATEGORY_AUDIO,
    "m4a": CATEGORY_AUDIO,

    # --- Archives ---
    "zip": CATEGORY_ARCHIVES,
    "rar": CATEGORY_ARCHIVES,
    "7z": CATEGORY_ARCHIVES,
    "tar": CATEGORY_ARCHIVES,
    "gz": CATEGORY_ARCHIVES,
    "bz2": CATEGORY_ARCHIVES,
    "iso": CATEGORY_ARCHIVES,        # disk image, flagged as judgment call
    "dmg": CATEGORY_ARCHIVES,        # disk image, flagged as judgment call
    "img": CATEGORY_ARCHIVES,        # disk image, flagged as judgment call

    # --- Application ---
    "exe": CATEGORY_APPLICATION,
    "msi": CATEGORY_APPLICATION,
    "app": CATEGORY_APPLICATION,
    "apk": CATEGORY_APPLICATION,
    "deb": CATEGORY_APPLICATION,
    "rpm": CATEGORY_APPLICATION,
    "dll": CATEGORY_APPLICATION,
    "so": CATEGORY_APPLICATION,
    "bat": CATEGORY_APPLICATION,

    # --- Fonts (not a top-level category; folded into Application) ---
    "ttf": CATEGORY_APPLICATION,
    "otf": CATEGORY_APPLICATION,
    "woff": CATEGORY_APPLICATION,
    "woff2": CATEGORY_APPLICATION,
}


def get_category(filename: str) -> str:
    """
    Return the broad category for a given filename based on its extension.
    Falls back to 'Uncategorized' if the extension is unknown — this should
    route to the metadata-only classifier per section 6.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return EXTENSION_CATEGORY_MAP.get(ext, "Uncategorized")


# if __name__ == "__main__":
#     # quick sanity check
#     samples = ["report.pdf", "main.py", "photo.HEIC", "movie.mkv", "song.flac",
#                "backup.tmp", "archive.zip", "setup.exe", "unknown.xyz"]
#     for s in samples:
#         print(f"{s:15s} -> {get_category(s)}")
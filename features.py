"""Turns a file into one text string for the classifier."""
import os
import re

from file_categories import get_category
from Files_Text_extractor import (
    extract_pdf_text, extract_docx_text, extract_pptx_text, extract_text_file, extract_code_text,
)


MIN_CONTENT_CHARS = 20  # shorter bodies (e.g. a stray "x" in a scanned page) count as unreadable


def build_text(path, max_chars=20000):
    """Returns (text, has_content). has_content is False when no body text could
    be read (scans, images, unsupported types) - those files fall back to
    filename + extension tokens only."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        body = extract_pdf_text(path)
    elif ext == ".docx":
        body = extract_docx_text(path)
    elif ext == ".pptx":
        body = extract_pptx_text(path)
    elif ext in (".txt", ".md"):
        body = extract_text_file(path)
    elif get_category(path) == "Code":
        body = extract_code_text(path)
    else:
        body = ""
    stem = os.path.splitext(os.path.basename(path))[0]
    name = "" if re.fullmatch(r"doc[_ ]?\d+", stem, re.I) else re.sub(r"[_\-.\d]+", " ", stem)  # placeholder names carry no information
    text = f"{name} ext_{ext.lstrip('.')} {body or ''}"[:max_chars]
    return text, len((body or "").strip()) >= MIN_CONTENT_CHARS

"""Runs every extractor against Test_Files/ and prints a readable report."""

import os

from Files_Text_extractor import (
    extract_pdf_text,
    extract_docx_text,
    extract_image_metadata,
    extract_text_file,
    extract_code_text,
)
from Language_Detector import detect_programming_language

TEST_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Test_Files")

PDF_EXTENSIONS = {".pdf"}
DOCX_EXTENSIONS = {".docx"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}
TEXT_EXTENSIONS = {".txt"}

PREVIEW_LENGTH = 300


def print_section(title):
    print(f"\n{'=' * 70}\n {title}\n{'=' * 70}")


def preview(text):
    if not text:
        return "(no text extracted)"
    text = text.strip()
    if len(text) > PREVIEW_LENGTH:
        return f"{text[:PREVIEW_LENGTH]}... [truncated, {len(text)} chars total]"
    return text


def test_pdf_file(file_path):
    print_section(f"PDF | {os.path.basename(file_path)}")
    print(preview(extract_pdf_text(file_path)))


def test_docx_file(file_path):
    print_section(f"DOCX | {os.path.basename(file_path)}")
    print(preview(extract_docx_text(file_path)))


def test_image_file(file_path):
    print_section(f"IMAGE | {os.path.basename(file_path)}")
    metadata = extract_image_metadata(file_path)
    if metadata:
        for key, value in metadata.items():
            print(f"  {key}: {value}")
    else:
        print("  (no EXIF metadata found)")


def test_text_file(file_path):
    print_section(f"TEXT | {os.path.basename(file_path)}")
    print(preview(extract_text_file(file_path)))


def test_code_file(file_path):
    print_section(f"CODE | {os.path.basename(file_path)}")
    print(f"  Detected Language: {detect_programming_language(file_path)}")
    print(preview(extract_code_text(file_path)))


DISPATCH_BY_EXTENSION = (
    (PDF_EXTENSIONS, test_pdf_file),
    (DOCX_EXTENSIONS, test_docx_file),
    (IMAGE_EXTENSIONS, test_image_file),
    (TEXT_EXTENSIONS, test_text_file),
)


def dispatch(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    for extensions, handler in DISPATCH_BY_EXTENSION:
        if extension in extensions:
            return handler(file_path)
    return test_code_file(file_path)


def run_tests():
    if not os.path.isdir(TEST_FILES_DIR):
        print(f"Test_Files directory not found at: {TEST_FILES_DIR}")
        return

    tested = 0
    for root, _, files in os.walk(TEST_FILES_DIR):
        for filename in sorted(files):
            dispatch(os.path.join(root, filename))
            tested += 1

    print(f"\n{'=' * 70}\n Done - tested {tested} file(s)\n{'=' * 70}")


if __name__ == "__main__":
    run_tests()

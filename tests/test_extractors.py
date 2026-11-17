import os
import pytest
from Files_Text_extractor import (extract_pdf_text, extract_docx_text, extract_image_metadata,
                                  extract_text_file, extract_code_text)

T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Test_Files")
def p(*a): return os.path.join(T, *a)

def test_pdf_text_extracted():
    assert "Invoice" in extract_pdf_text(p("pdf", "invoice.pdf"))

def test_pdf_long_paper():
    assert len(extract_pdf_text(p("pdf", "research_paper.pdf"))) > 500

def test_pdf_blank_page_has_no_real_text():
    assert len(extract_pdf_text(p("pdf", "blank_page.pdf")).strip()) <= 1

def test_pdf_corrupt_returns_empty(tmp_path):
    f = tmp_path / "bad.pdf"; f.write_bytes(b"not a pdf")
    assert extract_pdf_text(str(f)) == ""

def test_pdf_missing_returns_empty(tmp_path):
    assert extract_pdf_text(str(tmp_path / "none.pdf")) == ""

def test_docx_single_line():
    assert "minimal test case" in extract_docx_text(p("docx", "single_line.docx"))

def test_docx_blank_first_paragraph():
    assert "blank first paragraph" in extract_docx_text(p("docx", "empty_structure.docx"))

def test_docx_corrupt_returns_empty(tmp_path):
    f = tmp_path / "bad.docx"; f.write_bytes(b"junk")
    assert extract_docx_text(str(f)) == ""

def test_text_and_code_files(tmp_path):
    f = tmp_path / "a.txt"; f.write_text("héllo", encoding="utf-8")
    assert extract_text_file(str(f)) == "héllo" and extract_code_text(str(f)) == "héllo"

def test_text_file_missing_returns_none(tmp_path):
    assert extract_text_file(str(tmp_path / "none.txt")) is None

def test_image_metadata_is_dict_and_png_empty():
    assert isinstance(extract_image_metadata(p("images", "photo2.jpg")), dict)
    assert extract_image_metadata(p("images", "photo3.png")) == {}

def test_image_corrupt_returns_empty(tmp_path):
    f = tmp_path / "bad.jpg"; f.write_bytes(b"junk")
    assert extract_image_metadata(str(f)) == {}

import os
from features import build_text

T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Test_Files")

def test_pdf_has_content_and_name_tokens():
    text, ok = build_text(os.path.join(T, "pdf", "invoice.pdf"))
    assert ok and "Amount due" in text and "ext_pdf" in text

def test_image_is_metadata_only():
    text, ok = build_text(os.path.join(T, "images", "photo1.jpg"))
    assert not ok and "photo" in text and "ext_jpg" in text

def test_code_file_has_content():
    assert build_text(os.path.join(T, "code", "hello.py"))[1]

def test_tiny_body_below_threshold(tmp_path):
    f = tmp_path / "t.txt"; f.write_text("hi")
    assert not build_text(str(f))[1]

def test_blank_pdf_is_not_content():
    assert not build_text(os.path.join(T, "pdf", "blank_page.pdf"))[1]

def test_max_chars(tmp_path):
    f = tmp_path / "big.txt"; f.write_text("word " * 10000)
    assert len(build_text(str(f), max_chars=500)[0]) == 500

def test_unknown_extension(tmp_path):
    f = tmp_path / "data.xyz"; f.write_text("abc")
    assert build_text(str(f)) == ("data ext_xyz ", False)

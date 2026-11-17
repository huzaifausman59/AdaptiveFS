import os
import pytest
from Language_Detector import detect_programming_language as detect

C = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Test_Files", "code")

@pytest.mark.parametrize("name,lang", [
    ("hello.py", "Python"), ("app.js", "JavaScript"), ("Main.java", "Java"),
    ("matrix.cpp", "C++"), ("server.go", "Go"),
])
def test_sample_files(name, lang):
    assert detect(os.path.join(C, name)) == lang

def test_wrong_extension_falls_back_to_content(tmp_path):
    f = tmp_path / "script.txt"; f.write_text("package main\nfunc main() {\n fmt.Println(1)\n}")
    assert detect(str(f)) == "Go"

def test_no_keywords_unknown(tmp_path):
    f = tmp_path / "x.zzz"; f.write_text("12345")
    assert detect(str(f)) == "Unknown"

def test_missing_file_uses_extension(tmp_path):
    assert detect(str(tmp_path / "ghost.py")) == "Python"

def test_substring_false_positive_documented(tmp_path):
    # 'end' inside 'endpoint' should not make plain prose look like Ruby/Lua
    f = tmp_path / "notes.zzz"; f.write_text("the endpoint is down")
    assert detect(str(f)) == "Unknown"

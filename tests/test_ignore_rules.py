import pytest
from ignore_rules import DEFAULT_IGNORE_PATTERNS, load_ignore_config, should_ignore

@pytest.mark.parametrize("name", [
    "a.tmp", "b.crdownload", "c.part", "d.swp", "desktop.ini", "Thumbs.db", "~$report.docx",
])
def test_builtin_patterns_ignored(name):
    assert should_ignore(name, DEFAULT_IGNORE_PATTERNS)

@pytest.mark.parametrize("name", ["report.pdf", "notes.txt", "photo.jpg"])
def test_normal_files_not_ignored(name):
    assert not should_ignore(name, DEFAULT_IGNORE_PATTERNS)

def test_user_glob_and_extension(tmp_path):
    (tmp_path / ".adaptivefsignore").write_text("# c\ntest_*\n")
    (tmp_path / ".adaptivefsignore_ext").write_text("xlsx\n")
    cfg = load_ignore_config(str(tmp_path))
    assert should_ignore("test_a.txt", cfg["patterns"], cfg["extensions"])
    assert should_ignore("data.XLSX", cfg["patterns"], cfg["extensions"])
    assert not should_ignore("data.csv", cfg["patterns"], cfg["extensions"])

def test_no_config_files(tmp_path):
    cfg = load_ignore_config(str(tmp_path))
    assert cfg["extensions"] == set()

import os
import pytest
import sort
from sort import avoid_collision, resolve_destination, sort_file

@pytest.fixture(autouse=True)
def no_log(monkeypatch):
    monkeypatch.setattr(sort, "log_action", lambda **k: None)

def test_resolve_destination(tmp_path):
    assert resolve_destination(str(tmp_path / "a.pdf"), str(tmp_path)) == str(tmp_path / "Documents" / "a.pdf")

def test_collision_numbering(tmp_path):
    (tmp_path / "a.txt").write_text("x"); (tmp_path / "a (1).txt").write_text("x")
    assert avoid_collision(str(tmp_path / "a.txt")).endswith("a (2).txt")

def test_no_collision_returns_same(tmp_path):
    p = str(tmp_path / "new.txt")
    assert avoid_collision(p) == p

def test_sort_moves_file(tmp_path):
    f = tmp_path / "r.pdf"; f.write_bytes(b"%PDF")
    out = sort_file(str(f), str(tmp_path))
    assert out == str(tmp_path / "Documents" / "r.pdf") and os.path.isfile(out) and not f.exists()

def test_sort_never_overwrites(tmp_path):
    (tmp_path / "Documents").mkdir(); (tmp_path / "Documents" / "r.pdf").write_text("old")
    f = tmp_path / "r.pdf"; f.write_text("new")
    out = sort_file(str(f), str(tmp_path))
    assert out.endswith("r (1).pdf") and (tmp_path / "Documents" / "r.pdf").read_text() == "old"

def test_missing_file_is_skipped(tmp_path):
    p = str(tmp_path / "ghost.pdf")
    assert sort_file(p, str(tmp_path)) == p

def test_file_already_in_place(tmp_path):
    (tmp_path / "Documents").mkdir(); f = tmp_path / "Documents" / "a.pdf"; f.write_text("x")
    assert sort_file(str(f), str(tmp_path)) == str(f) and f.exists()

def test_classifier_category_overrides_extension(tmp_path):
    f = tmp_path / "scan.pdf"; f.write_bytes(b"%PDF")
    out = sort_file(str(f), str(tmp_path), category="Finance")
    assert out == str(tmp_path / "Finance" / "scan.pdf")

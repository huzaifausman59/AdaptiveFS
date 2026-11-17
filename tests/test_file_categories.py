import pytest
from file_categories import get_category

@pytest.mark.parametrize("name,expected", [
    ("report.pdf", "Documents"), ("REPORT.PDF", "Documents"),
    ("main.py", "Code"), ("photo.jpg", "Images"),
    ("unknown.xyz", "Uncategorized"), ("noextension", "Uncategorized"),
    ("archive.zip", "Archives"), ("my.report.v2.pdf", "Documents"),
])
def test_get_category(name, expected):
    assert get_category(name) == expected

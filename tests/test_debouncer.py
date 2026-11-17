import time
from debouncer import Debouncer

def test_burst_gives_one_callback(tmp_path):
    f = tmp_path / "a.txt"; f.write_text("x")
    calls = []
    d = Debouncer(calls.append, quiet=0.2, settle=0.05)
    for _ in range(5):
        d.touch(str(f)); time.sleep(0.05)
    time.sleep(0.6)
    assert calls == [str(f)]

def test_growing_file_waits_until_stable(tmp_path):
    f = tmp_path / "big.bin"; f.write_bytes(b"a")
    calls = []
    d = Debouncer(calls.append, quiet=0.2, settle=0.3)
    d.touch(str(f))
    time.sleep(0.3); f.write_bytes(b"aaaa")        # grows during the settle check
    time.sleep(0.2)
    assert calls == []                              # not fired while changing
    time.sleep(1.0)
    assert calls == [str(f)]                        # fired once it stopped changing

def test_deleted_file_is_dropped(tmp_path):
    f = tmp_path / "t.tmp"; f.write_text("x")
    calls = []
    d = Debouncer(calls.append, quiet=0.1, settle=0.05)
    d.touch(str(f)); f.unlink()
    time.sleep(0.5)
    assert calls == []

def test_independent_files(tmp_path):
    a, b = tmp_path / "a.txt", tmp_path / "b.txt"; a.write_text("1"); b.write_text("2")
    calls = []
    d = Debouncer(calls.append, quiet=0.1, settle=0.05)
    d.touch(str(a)); d.touch(str(b)); time.sleep(0.5)
    assert sorted(calls) == sorted([str(a), str(b)])

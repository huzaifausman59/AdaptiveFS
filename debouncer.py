"""Collapses bursts of filesystem events into one callback per file."""
import os
import threading
import time


class Debouncer:
    """Calls callback(path) once `path` has had no events for `quiet` seconds
    and its size is stable (so half-downloaded files are never processed)."""

    def __init__(self, callback, quiet=2.0, settle=0.5):
        self.callback, self.quiet, self.settle = callback, quiet, settle
        self._timers, self._lock = {}, threading.Lock()

    def touch(self, path):
        with self._lock:
            if path in self._timers:
                self._timers[path].cancel()
            timer = threading.Timer(self.quiet, self._fire, args=(path,))
            timer.daemon = True
            self._timers[path] = timer
            timer.start()

    def _fire(self, path):
        with self._lock:
            self._timers.pop(path, None)
        try:
            size = os.path.getsize(path)
            time.sleep(self.settle)
            if size != os.path.getsize(path):
                return self.touch(path)  # still being written
        except OSError:
            return  # file vanished (temp file renamed or deleted)
        self.callback(path)

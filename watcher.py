import os
import sys
import threading
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from sort import sort_file
from ignore_rules import load_ignore_config, should_ignore
from command_handler import handle_command
from debouncer import Debouncer
from features import build_text
import classifier

MODEL_PATH = "model.joblib"
TAU = 0.6            # confidence gate: below this, the file goes to _Review
REVIEW_FOLDER = "_Review"


class AdaptiveFSHandler(FileSystemEventHandler):
    """Detects filesystem events, debounces them, then classifies each stable
    file. With auto=True the file is moved (confident -> predicted category,
    unsure -> _Review); otherwise the decision is only printed."""

    def __init__(self, base_dir, ignore_config, model=None, auto=False):
        super().__init__()
        self.base_dir = os.path.abspath(base_dir)
        self.patterns = ignore_config["patterns"]
        self.ignored_extensions = ignore_config["extensions"]
        self.model, self.auto = model, auto
        self.debouncer = Debouncer(self.process)

    def _queue(self, path):
        if should_ignore(path, self.patterns, self.ignored_extensions):
            print(f"[IGNORED]   {path}")
            return
        self.debouncer.touch(path)

    def process(self, path):
        # Only handle files directly in the watched folder (not already sorted ones)
        if os.path.dirname(os.path.abspath(path)) != self.base_dir or not os.path.isfile(path):
            return
        if self.model is None:
            category, conf = None, None
        else:
            text, _ = build_text(path)
            category, conf = classifier.predict(self.model, text)
        print(f"[DECISION]  {os.path.basename(path)} -> {category} (conf={conf})")
        if not self.auto:
            return
        if category is not None and conf < TAU:
            category = REVIEW_FOLDER
        sort_file(path, self.base_dir, method="watcher", category=category)

    def on_created(self, event):
        if not event.is_directory:
            print(f"[CREATED]   {event.src_path}")
            self._queue(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._queue(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            print(f"[MOVED]     {event.src_path}  -->  {event.dest_path}")
            self._queue(event.dest_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[DELETED]   {event.src_path}")


def input_listener(folder):
    """Thin read-print loop. All actual command logic lives in
    command_handler.handle_command so it can be tested independently
    of stdin."""
    while True:
        command = input("> ").strip()

        if command == "quit":
            break

        if not command:
            continue

        result = handle_command(command, folder)
        print(result)


def watch_folder(path_to_watch, auto=False):
    print(f"Watching folder: {path_to_watch}  (auto-sort {'ON' if auto else 'OFF'})")
    print("Press Ctrl+C to stop.\n")

    model = classifier.load(MODEL_PATH) if os.path.isfile(MODEL_PATH) else None
    if model is None:
        print(f"[WARN] {MODEL_PATH} not found - run train_model.py. Falling back to extension categories.")

    ignore_config = load_ignore_config(path_to_watch)

    event_handler = AdaptiveFSHandler(path_to_watch, ignore_config, model=model, auto=auto)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()

    listener_thread = threading.Thread(target=input_listener, args=(path_to_watch,), daemon=True)
    listener_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nWatcher stopped.")

    observer.join()


if __name__ == "__main__":
    # Usage: python watcher.py [folder] [--auto]
    args = [a for a in sys.argv[1:] if a != "--auto"]
    folder = args[0] if args else "./test_folder"
    watch_folder(folder, auto="--auto" in sys.argv)

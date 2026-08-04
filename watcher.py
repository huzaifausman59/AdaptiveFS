import sys
import threading
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from sort import sort_file
from ignore_rules import load_ignore_config, should_ignore
from command_handler import handle_command


class AdaptiveFSHandler(FileSystemEventHandler):
    """Detects filesystem events. Currently only CREATED events are
    sorted automatically (method="watcher"); everything else is just
    logged to the console."""

    def __init__(self, base_dir, ignore_config):
        super().__init__()
        self.base_dir = base_dir
        self.patterns = ignore_config["patterns"]
        self.ignored_extensions = ignore_config["extensions"]

    def on_created(self, event):
        if event.is_directory:
            return

        if should_ignore(event.src_path, self.patterns, self.ignored_extensions):
            print(f"[IGNORED]   {event.src_path}")
            return

        print(f"[CREATED]   {event.src_path}")
        #sort_file(event.src_path, self.base_dir, method="watcher")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[MODIFIED]  {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[DELETED]   {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"[MOVED]     {event.src_path}  -->  {event.dest_path}")


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


def watch_folder(path_to_watch):
    print(f"Watching folder: {path_to_watch}")
    print("Press Ctrl+C to stop.\n")

    ignore_config = load_ignore_config(path_to_watch)

    event_handler = AdaptiveFSHandler(base_dir=path_to_watch, ignore_config=ignore_config)
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
    #  Folder you want to watch
    folder = "./test_folder"

    # Or pass a folder as a command-line argument:
    # python watcher.py "C:/Users/You/Downloads"

    if len(sys.argv) > 1:
        folder = sys.argv[1]

    watch_folder(folder)
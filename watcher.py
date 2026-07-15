import sys
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sort import sort_file
import os


class AdaptiveFSHandler(FileSystemEventHandler):
    """Handles file system events and prints them to the terminal."""

    def __init__(self, base_dir):
        super().__init__()
        self.base_dir = base_dir

    def on_created(self, event):
        if not event.is_directory:
            print(f"[CREATED]   {event.src_path}")
            #sort_file(event.src_path, self.base_dir)

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
    while True:
        command = input("> ").strip()

        if command == "quit":
            break

        elif command == "list":
            for name in os.listdir(folder):
                path = os.path.join(folder, name)
                if os.path.isfile(path):
                    print(name)

        elif command == "all":
            for name in os.listdir(folder):
                path = os.path.join(folder, name)
                if os.path.isfile(path):
                    sort_file(path, folder)

        else:
            path = os.path.join(folder, command)
            if os.path.isfile(path):
                sort_file(path, folder)
            else:
                print("File not found.")

def watch_folder(path_to_watch):
    print(f"Watching folder: {path_to_watch}")
    print("Press Ctrl+C to stop.\n")

    event_handler = AdaptiveFSHandler(base_dir=path_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
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
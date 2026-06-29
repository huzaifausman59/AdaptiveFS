import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class AdaptiveFSHandler(FileSystemEventHandler):
    """Handles file system events and prints them to the terminal."""

    def on_created(self, event):
        if not event.is_directory:
            print(f"[CREATED]   {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[MODIFIED]  {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[DELETED]   {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"[MOVED]     {event.src_path}  -->  {event.dest_path}")


def watch_folder(path_to_watch):
    print(f"Watching folder: {path_to_watch}")
    print("Press Ctrl+C to stop.\n")

    event_handler = AdaptiveFSHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

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
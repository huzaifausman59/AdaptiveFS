import sys
import time
import logging
import csv
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ── Configure Python's logging module (for console output) ──────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("AdaptiveFS")


# ── CSV log file setup ───────────────────────────────────────────────────────
LOG_FILE = "events_log.csv"

def init_csv_log():
    """Create the CSV file with headers if it doesn't exist yet."""
    log_path = Path(LOG_FILE)
    if not log_path.exists():
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "event_type", "file_path", "dest_path"])


def write_event_to_csv(event_type, src_path, dest_path=""):
    """Append a single event row to the CSV log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, event_type, src_path, dest_path])


# ── Event Handler ────────────────────────────────────────────────────────────
class LoggingFSHandler(FileSystemEventHandler):
    """Handles file system events, logs to console AND CSV."""

    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"[CREATED]   {event.src_path}")
            write_event_to_csv("CREATED", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            logger.info(f"[MODIFIED]  {event.src_path}")
            write_event_to_csv("MODIFIED", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            logger.info(f"[DELETED]   {event.src_path}")
            write_event_to_csv("DELETED", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            logger.info(f"[MOVED]     {event.src_path}  -->  {event.dest_path}")
            write_event_to_csv("MOVED", event.src_path, event.dest_path)


# ── Main ─────────────────────────────────────────────────────────────────────
def watch_folder(path_to_watch):
    init_csv_log()
    logger.info(f"Watching folder: {path_to_watch}")
    logger.info(f"Logging events to: {LOG_FILE}")
    logger.info("Press Ctrl+C to stop.\n")

    event_handler = LoggingFSHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Watcher stopped.")

    observer.join()


if __name__ == "__main__":
    folder = "./test_folder"

    if len(sys.argv) > 1:
        folder = sys.argv[1]

    watch_folder(folder)
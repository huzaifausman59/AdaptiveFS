"""
AdaptiveFS — Actions Log

Records every actual sort decision AdaptiveFS makes: where a file came
from, where it ended up, when, and how the move was triggered (watcher
auto-detection vs. manual input). This is distinct from events_log.csv
(raw filesystem activity via watcher_logger.py) — this log is the
"what did the system decide to do" record, i.e. the Activity Log
described in proposal section 4.5.

CSV columns: original_path, destination, timestamp, method
"""

import csv
import os
from datetime import datetime

LOG_FILENAME = "actions_log.csv"
LOG_HEADER = ["original_path", "destination", "timestamp", "method"]


def log_action(original_path: str, destination: str, method: str, log_path: str = LOG_FILENAME) -> None:
    """
    Appends one action record to the actions log CSV. Creates the file
    with a header row if it doesn't exist yet.

    original_path : where the file was before the action
    destination   : where the file ended up
    method        : how the action was triggered, e.g. "watcher" or "manual"
    log_path      : path to the CSV file (defaults to actions_log.csv
                     in the current working directory)
    """
    file_exists = os.path.isfile(log_path)

    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(LOG_HEADER)

        timestamp = datetime.now().isoformat(timespec="seconds")
        writer.writerow([original_path, destination, timestamp, method])


if __name__ == "__main__":
    # quick manual test
    test_log = "test_actions_log.csv"
    log_action("./test_folder/report.pdf", "./test_folder/Documents/report.pdf", "manual", log_path=test_log)
    log_action("./test_folder/photo.jpg", "./test_folder/Images/photo.jpg", "watcher", log_path=test_log)

    with open(test_log, "r", encoding="utf-8") as f:
        print(f.read())

    os.remove(test_log)

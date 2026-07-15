# AdaptiveFS

An intelligent file system watcher that monitors a folder for new files,
classifies them by type, and organizes them into category folders —
either automatically or under manual control while the classification
and sorting logic is still being tested. Built with Python and watchdog
as part of an adaptive file organization pipeline.

---

## Project Structure

AdaptiveFS/

├── adaptivefs-env/         ← virtual environment (not committed to Git)

├── test_folder/            ← folder used for local testing

├── watcher.py               ← watches a folder, dispatches CREATED events to the sorter, runs the manual command thread

├── watcher_logger.py         ← standalone watcher that logs raw filesystem events to CSV

├── sort.py                  ← resolves destination, avoids naming collisions, moves the file, triggers logging

├── file_categories.py        ← extension → category mapping (`get_category()`)

├── ignore_rules.py           ← combines glob-pattern and extension ignore checks (`should_ignore()`)

├── extension_rules.py        ← standalone extension-based ignore check, used by ignore_rules.py

├── command_handler.py        ← interprets manual commands (`list` / `all` / `<filename>`) typed into the watcher's input thread

├── logger.py                 ← writes every actual sort action to actions_log.csv

├── events_log.csv           ← raw filesystem event log (auto-created by watcher_logger.py)

├── actions_log.csv           ← log of files actually sorted: original path, destination, timestamp, method (auto-created by logger.py)

├── .adaptivefsignore         ← optional, per-watched-folder: glob patterns to never sort (e.g. `test_*`)

├── .adaptivefsignore_ext     ← optional, per-watched-folder: file extensions to never sort (e.g. `xlsx`)

├── findings.md               ← Phase 1 observations and notes

├── requirements.txt          ← Python dependencies

├── .gitignore

└── README.md

---

## Requirements

- Python 3.11 or higher
- pip

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AdaptiveFS.git
cd AdaptiveFS
```

### 2. Create and activate virtual environment
```bash
# Create
python -m venv adaptivefs-env

# Activate on Windows
adaptivefs-env\Scripts\activate

# Activate on Mac/Linux
source adaptivefs-env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

### Sorting watcher (current main entry point)
```bash
python watcher.py
python watcher.py "C:\Users\YourName\Downloads"
```

This watches the given folder (`./test_folder` by default) for new files.
New files are **not** moved automatically the moment they appear — instead:

- `[CREATED]` is printed and the file is sorted immediately if it doesn't
  match an ignore rule (`method="watcher"` in the log)
- Files matching a glob pattern in `.adaptivefsignore` or an extension
  listed in `.adaptivefsignore_ext` are skipped and printed as `[IGNORED]`

Alongside the watcher, an input thread reads commands from the terminal:

| Command | Effect |
|---|---|
| `list` | List sortable (non-ignored) files currently in the watched folder |
| `all` | Sort every sortable file in the watched folder |
| `<filename>` | Sort that specific file — but still respects ignore rules; an ignored file typed by name is left alone |
| `quit` | Stop the input thread (watcher keeps running; Ctrl+C stops everything) |

### Raw event logger (unchanged, standalone)
```bash
python watcher_logger.py
python watcher_logger.py "C:\Users\YourName\Downloads"
```

Logs every raw filesystem event (created/modified/deleted/moved) to
`events_log.csv` with timestamp, event type, and file path — this is
independent of sorting and is mainly useful for debugging watcher
behavior itself.

---

## How Sorting Works

1. `file_categories.py` maps a file's extension to a broad category
   (Code, Documents, Images, Videos, Temporary, Audio, Archives,
   Application). Unknown extensions fall back to `Uncategorized`.
2. `ignore_rules.py` checks the file against `.adaptivefsignore` (glob
   patterns) and `.adaptivefsignore_ext` (extensions) before anything
   is touched.
3. `sort.py` resolves the destination folder, avoids overwriting an
   existing file of the same name (appends `(1)`, `(2)`, ...), moves
   the file, and records the action.
4. `logger.py` appends a row to `actions_log.csv` — original path,
   destination, timestamp, and method (`watcher` or `manual`) — for
   every file actually moved.

Currently the watcher only monitors the top level of the watched
folder (`recursive=False`); subfolder support is planned but not yet
implemented.

---

## Event Types Monitored (watcher_logger.py)

| Event | Description |
|-------|-------------|
| CREATED | A new file was created |
| MODIFIED | An existing file was changed |
| DELETED | A file was removed |
| MOVED | A file was renamed or moved |

---

## Team

- huzaifa
- abu huraira
- ali adnan

---

## Phase Progress

- [x] Phase 1: Folder watcher with event logging
- [x] Phase 2: Extension-based classification, sorting into category folders, ignore rules (glob + extension), manual command control, action logging
- [ ] Phase 3: Work on extracting Context from files
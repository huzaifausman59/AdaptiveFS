# AdaptiveFS

An intelligent file system watcher that monitors folders for file events 
(created, modified, deleted, moved) and logs them for further processing. 
Built with Python and watchdog as part of an adaptive file organization pipeline.

---

## Project Structure

AdaptiveFS/

├── adaptivefs-env/       ← virtual environment (not committed to Git)

├── test_folder/          ← folder used for local testing

├── watcher.py            ← basic event printer

├── watcher_logger.py     ← logs events to CSV with timestamps

├── events_log.csv        ← generated log file (auto-created on run)

├── findings.md           ← Phase 1 observations and notes

├── requirements.txt      ← Python dependencies

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

### Basic watcher (prints to terminal)
```bash
python watcher.py
```

### Watch a specific folder
```bash
python watcher.py "C:\Users\YourName\Downloads"
```

### Logging watcher (saves events to CSV)
```bash
python watcher_logger.py
python watcher_logger.py "C:\Users\YourName\Downloads"
```

Events are saved to `events_log.csv` with timestamp, event type, and file path.

---

## Event Types Monitored

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
- [ ] Phase 2: Coming soon

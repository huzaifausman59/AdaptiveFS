# Phase 1 Watcher Findings

## Test Environment
- OS: Windows 11 
- Python version: 3.13.5
- Watchdog version: 6.0.0
- Watched folders: test_folder, Downloads


## Observations

### Event Patterns
- Saving a new file triggers: CREATED + MODIFIED (two events for one action)
- Browser downloads fire multiple MODIFIED events as the file downloads in chunks
- Some apps write to a temp `.tmp` file first, then fire a MOVED event to the final name
- Renaming a file fires a MOVED event (src = old name, dest = new name)
- Deleting a file fires a single DELETED event

### Unexpected Behaviors
- Temp files (`.tmp`, `.crdownload`) appear frequently as intermediary writes
- Some editors delete and recreate the file instead of modifying it in place

### File Types With Most Events
- .docx files: high event count due to temp file writes by Word
- .tmp files: appear frequently as intermediary writes
- Browser downloads: continuous MODIFIED stream until download completes

### Edge Cases to Handle in Pipeline
- Duplicate events for single user action — need deduplication or debounce logic
- Temp files should be filtered out before processing
- Very large files fire many MODIFIED events — should wait for file to stop changing before acting

## Conclusions
The watcher works reliably across all tested event types. The main design 
challenge for AdaptiveFS will be filtering noise (duplicate events, temp files) 
before passing events downstream to the classification and organization pipeline.
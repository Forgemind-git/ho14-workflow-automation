"""
Sample 03 -- File Drop Watcher & Processor
Watches an input/ folder for new CSV files. When one appears, reads it,
computes a summary (row count, column totals), writes a processed_ prefixed
copy to output/, and moves the original to processed/.

Libraries: watchdog, csv, shutil
"""

import os
import csv
import time
import logging
import datetime
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# -- Configuration (override via .env) ----------------------------------------
INPUT_DIR = os.getenv("INPUT_DIR", "input")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
PROCESSED_DIR = os.getenv("PROCESSED_DIR", "processed")
LOG_FILE = os.getenv("LOG_FILE", "run.log")
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "2.0"))
# How long (seconds) to wait after detecting a file before reading it
# (allows slow copies to finish)
FILE_SETTLE_DELAY = float(os.getenv("FILE_SETTLE_DELAY", "1.0"))

# -- Logging setup ------------------------------------------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def ensure_dirs():
    """Create input/, output/, and processed/ if they do not exist."""
    for d in [INPUT_DIR, OUTPUT_DIR, PROCESSED_DIR]:
        Path(d).mkdir(parents=True, exist_ok=True)


def numeric_summary(rows, fieldnames):
    """
    Compute per-column totals for numeric columns.
    Returns a dict of {col_name: total}.
    Non-numeric columns are skipped.
    """
    totals = {}
    for col in fieldnames:
        col_values = []
        for row in rows:
            try:
                col_values.append(float(row[col]))
            except (ValueError, TypeError):
                pass
        if col_values:
            totals[col] = sum(col_values)
    return totals


def process_csv(src_path):
    """
    Read a CSV file, compute summary, write processed copy, move original.
    Returns a dict with processing results, or None on error.
    """
    src = Path(src_path)
    if not src.exists():
        log.warning("File vanished before processing: %s", src)
        return None

    # Wait for file to settle (finish being written)
    time.sleep(FILE_SETTLE_DELAY)

    log.info("Processing: %s", src.name)
    print("\n[{}] Processing: {}".format(
        datetime.datetime.now().strftime("%H:%M:%S"), src.name))

    try:
        with open(src, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames or []
    except Exception as exc:
        log.error("Failed to read %s: %s", src.name, exc)
        print("  [ERROR] Could not read file: {}".format(exc))
        return None

    if not rows:
        log.warning("Empty CSV (0 data rows): %s", src.name)
        print("  [WARN]  File has no data rows.")
        return None

    # Compute summary
    row_count = len(rows)
    totals = numeric_summary(rows, fieldnames)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write processed_ copy to output/
    out_name = "processed_{}".format(src.name)
    out_path = Path(OUTPUT_DIR) / out_name
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames + ["__processed_at"])
        writer.writeheader()
        for row in rows:
            row["__processed_at"] = timestamp
            writer.writerow(row)

    # Move original to processed/
    dest_path = Path(PROCESSED_DIR) / src.name
    # If a file with this name already exists in processed/, add a timestamp suffix
    if dest_path.exists():
        stem = src.stem
        suffix = src.suffix
        dest_path = Path(PROCESSED_DIR) / "{}_{}{}".format(
            stem, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), suffix
        )
    shutil.move(str(src), str(dest_path))

    result = {
        "source": src.name,
        "row_count": row_count,
        "columns": len(fieldnames),
        "numeric_totals": totals,
        "output": str(out_path),
        "archived": str(dest_path),
    }

    log.info(
        "Done: %s | rows=%d | cols=%d | output=%s",
        src.name, row_count, len(fieldnames), out_path
    )

    # Console summary
    print("  Rows     : {}".format(row_count))
    print("  Columns  : {} ({})".format(len(fieldnames), ", ".join(fieldnames)))
    if totals:
        print("  Totals   :")
        for col, total in totals.items():
            print("    {} = {:.2f}".format(col, total))
    print("  Output   : {}".format(out_path))
    print("  Archived : {}".format(dest_path))

    return result


class CSVDropHandler(FileSystemEventHandler):
    """Watchdog event handler that processes newly created .csv files."""

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() != ".csv":
            return
        log.info("Detected new file: %s", path.name)
        process_csv(str(path))

    def on_moved(self, event):
        """Also handle files moved/renamed into the input folder."""
        if event.is_directory:
            return
        path = Path(event.dest_path)
        if path.suffix.lower() != ".csv" or not str(path.parent.resolve()).endswith(
            str(Path(INPUT_DIR).resolve())
        ):
            return
        log.info("Detected moved file: %s", path.name)
        process_csv(str(path))


def process_existing_files():
    """Process any CSV files already in input/ at startup."""
    input_path = Path(INPUT_DIR)
    existing = list(input_path.glob("*.csv"))
    if existing:
        print("[startup] Found {} existing CSV file(s) in input/ -- processing now".format(
            len(existing)))
        log.info("Processing %d pre-existing file(s)", len(existing))
        for f in existing:
            process_csv(str(f))
    else:
        print("[startup] No existing files in input/ -- watching for new ones...")


def main():
    run_start = datetime.datetime.now()
    log.info("=" * 60)
    log.info("File watcher started | input=%s | output=%s | processed=%s",
             INPUT_DIR, OUTPUT_DIR, PROCESSED_DIR)

    ensure_dirs()

    # Process files already in the drop folder
    process_existing_files()

    # Start watchdog observer
    event_handler = CSVDropHandler()
    observer = Observer()
    observer.schedule(event_handler, path=INPUT_DIR, recursive=False)
    observer.start()

    print("\n" + "=" * 55)
    print("  File Drop Watcher -- Active")
    print("=" * 55)
    print("  Watching  : {}/".format(INPUT_DIR))
    print("  Output    : {}/".format(OUTPUT_DIR))
    print("  Archived  : {}/".format(PROCESSED_DIR))
    print("  Log       : {}".format(LOG_FILE))
    print("  Drop a .csv into input/ to process it.")
    print("  Press Ctrl+C to stop.")
    print("=" * 55 + "\n")

    try:
        while True:
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
        log.info("Watcher stopped by user (Ctrl+C)")
        print("\n[stopped] Watcher shut down cleanly.")

    observer.join()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

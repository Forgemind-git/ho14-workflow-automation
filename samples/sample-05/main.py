"""
Sample 05 -- Two-Source Sync Job
Reads records from a primary source (CSV A) and a secondary source (CSV B),
identifies rows in A missing from B (keyed on an ID column),
appends them to B, and logs the sync delta.

Libraries: csv, json
"""

import os
import csv
import json
import logging
import datetime
from pathlib import Path

# -- Configuration (override via .env) ----------------------------------------
SOURCE_A = os.getenv("SOURCE_A", "source_a.csv")
SOURCE_B = os.getenv("SOURCE_B", "source_b.csv")
ID_COLUMN = os.getenv("ID_COLUMN", "id")
LOG_FILE = os.getenv("LOG_FILE", "run.log")
DELTA_LOG = os.getenv("DELTA_LOG", "delta_log.jsonl")

# -- Logging setup ------------------------------------------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# -- CSV helpers --------------------------------------------------------------

def read_csv(path):
    """
    Read a CSV file and return (fieldnames, rows).
    rows is a list of dicts. fieldnames is the ordered list of column names.
    Returns (None, []) if the file does not exist.
    """
    p = Path(path)
    if not p.exists():
        return None, []

    with open(p, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    return fieldnames, rows


def write_csv(path, fieldnames, rows):
    """Write rows to a CSV file, creating or overwriting it."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_rows_to_csv(path, fieldnames, new_rows):
    """Append rows to an existing CSV (or create if not exists)."""
    p = Path(path)
    if not p.exists():
        write_csv(path, fieldnames, new_rows)
        return

    with open(p, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for row in new_rows:
            # Only write keys that match the existing CSV schema
            filtered = {k: row.get(k, "") for k in fieldnames}
            writer.writerow(filtered)


def extract_ids(rows, id_col):
    """Return a set of ID values from a list of rows."""
    return {str(row.get(id_col, "")).strip() for row in rows if row.get(id_col)}


# -- Delta logging ------------------------------------------------------------

def append_delta(delta_log_path, delta_record):
    """Append a JSON Lines delta record to the delta log."""
    with open(delta_log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(delta_record) + "\n")


# -- Main ---------------------------------------------------------------------

def main():
    run_start = datetime.datetime.now()
    run_ts = run_start.strftime("%Y-%m-%d %H:%M:%S")

    log.info("-" * 60)
    log.info("Run started | source_a=%s | source_b=%s | id_col=%s",
             SOURCE_A, SOURCE_B, ID_COLUMN)

    # -- Load source A (primary) ----------------------------------------------
    fields_a, rows_a = read_csv(SOURCE_A)
    if fields_a is None:
        log.error("Source A not found: %s", SOURCE_A)
        print("[ERROR] Source A not found: {}".format(SOURCE_A))
        return 1

    if not rows_a:
        log.warning("Source A is empty: %s", SOURCE_A)
        print("[WARN]  Source A has no data rows.")
        return 0

    if ID_COLUMN not in fields_a:
        log.error("ID column '%s' not found in Source A. Available: %s",
                  ID_COLUMN, fields_a)
        print("[ERROR] ID column '{}' not in Source A columns: {}".format(
            ID_COLUMN, ", ".join(fields_a)))
        return 1

    ids_a = extract_ids(rows_a, ID_COLUMN)
    log.info("Source A: %d rows, %d unique IDs", len(rows_a), len(ids_a))

    # -- Load source B (secondary) --------------------------------------------
    fields_b, rows_b = read_csv(SOURCE_B)

    if fields_b is None:
        # Source B does not exist yet -- treat as empty, use Source A schema
        log.info("Source B not found; will create it: %s", SOURCE_B)
        print("[INFO]  Source B does not exist -- will create it.")
        fields_b = fields_a
        rows_b = []
        ids_b = set()
    else:
        if not rows_b:
            ids_b = set()
        else:
            ids_b = extract_ids(rows_b, ID_COLUMN)
        log.info("Source B: %d rows, %d unique IDs", len(rows_b), len(ids_b))

    # -- Find delta (rows in A missing from B) --------------------------------
    missing_ids = ids_a - ids_b
    missing_rows = [
        row for row in rows_a
        if str(row.get(ID_COLUMN, "")).strip() in missing_ids
    ]

    if not missing_rows:
        log.info("No missing rows -- sources are in sync.")
        elapsed = (datetime.datetime.now() - run_start).total_seconds()

        # Still write a delta record showing a clean sync
        delta = {
            "synced_at": run_ts,
            "source_a_rows": len(rows_a),
            "source_b_rows": len(rows_b),
            "appended": 0,
            "missing_ids": [],
            "status": "IN_SYNC",
        }
        append_delta(DELTA_LOG, delta)
        log.info("Run complete | elapsed=%.2fs | status=IN_SYNC", elapsed)

        print("\n" + "=" * 55)
        print("  Sync Job -- Run Complete")
        print("=" * 55)
        print("  Source A : {} ({} rows)".format(SOURCE_A, len(rows_a)))
        print("  Source B : {} ({} rows)".format(SOURCE_B, len(rows_b)))
        print("  Delta    : 0 rows to sync -- sources are IN SYNC")
        print("  Elapsed  : {:.2f}s".format(elapsed))
        print("=" * 55 + "\n")
        return 0

    # -- Append missing rows to B ---------------------------------------------
    # Determine merged field list: all fields from B, plus any new fields from A
    merged_fields = list(fields_b)
    for col in fields_a:
        if col not in merged_fields:
            merged_fields.append(col)

    # Add sync metadata to each new row
    synced_rows = []
    for row in missing_rows:
        enriched = dict(row)
        enriched["__synced_at"] = run_ts
        synced_rows.append(enriched)

    # Add __synced_at to schema if not already there
    if "__synced_at" not in merged_fields:
        merged_fields.append("__synced_at")

    append_rows_to_csv(SOURCE_B, merged_fields, synced_rows)

    # Reload B to get updated count
    _, updated_rows_b = read_csv(SOURCE_B)
    new_b_count = len(updated_rows_b)

    # -- Write delta log ------------------------------------------------------
    delta = {
        "synced_at": run_ts,
        "source_a_rows": len(rows_a),
        "source_b_rows_before": len(rows_b),
        "source_b_rows_after": new_b_count,
        "appended": len(missing_rows),
        "missing_ids": sorted(list(missing_ids)),
        "status": "SYNCED",
    }
    append_delta(DELTA_LOG, delta)

    elapsed = (datetime.datetime.now() - run_start).total_seconds()
    log.info(
        "Run complete | appended=%d | b_rows_after=%d | elapsed=%.2fs | status=SYNCED",
        len(missing_rows), new_b_count, elapsed,
    )

    # -- Console summary -------------------------------------------------------
    print("\n" + "=" * 55)
    print("  Sync Job -- Run Complete")
    print("=" * 55)
    print("  Source A     : {} ({} rows)".format(SOURCE_A, len(rows_a)))
    print("  Source B     : {} ({} rows -> {} rows)".format(
        SOURCE_B, len(rows_b), new_b_count))
    print("  Appended     : {} new row(s)".format(len(missing_rows)))
    print("  IDs synced   :")
    for rid in sorted(missing_ids):
        print("    + {}".format(rid))
    print("  Delta log    : {}".format(DELTA_LOG))
    print("  Elapsed      : {:.2f}s".format(elapsed))
    print("=" * 55 + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

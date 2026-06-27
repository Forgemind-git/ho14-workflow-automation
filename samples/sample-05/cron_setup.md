# Cron Setup: Two-Source Sync Job

## 1. Create a virtual environment

All libraries used (`csv`, `json`) are part of Python's standard library.
No pip install is required.

```bash
cd /path/to/sample-05
python3 -m venv .venv
```

## 2. Configure your environment

```bash
cp .env.example .env
nano .env
```

Set:
- `SOURCE_A` -- path to your primary/authoritative CSV
- `SOURCE_B` -- path to the CSV that will receive missing rows
- `ID_COLUMN` -- the column name used as the unique key (e.g. `id`, `email`, `order_id`)

## 3. Test with the sample files

The repo includes `source_a.csv` (4 records) and `source_b.csv` (2 records).
IDs 1003 and 1004 are in A but not B.

```bash
bash run.sh
```

Expected output:
```
=======================================================
  Sync Job -- Run Complete
=======================================================
  Source A     : source_a.csv (4 rows)
  Source B     : source_b.csv (2 rows -> 4 rows)
  Appended     : 2 new row(s)
  IDs synced   :
    + 1003
    + 1004
  Delta log    : delta_log.jsonl
  Elapsed      : 0.01s
=======================================================
```

Run again -- it should report IN SYNC (idempotent):
```
  Delta    : 0 rows to sync -- sources are IN SYNC
```

## 4. Inspect the delta log

```bash
cat delta_log.jsonl
# {"synced_at": "2026-06-27 08:00:01", "source_a_rows": 4, "source_b_rows_before": 2, ...}
# {"synced_at": "2026-06-27 08:05:01", ..., "appended": 0, "status": "IN_SYNC"}
```

## 5. Add to crontab (runs every 6 hours)

```bash
crontab -e
```

Add this line:
```
0 */6 * * * /path/to/sample-05/run.sh >> /path/to/sample-05/cron.log 2>&1
```

Other schedule examples:
```
# Every 15 minutes
*/15 * * * * /path/to/sample-05/run.sh >> /path/to/sample-05/cron.log 2>&1

# Daily at midnight
0 0 * * * /path/to/sample-05/run.sh >> /path/to/sample-05/cron.log 2>&1
```

## 6. Verify it ran

```bash
# Check run log
tail -20 /path/to/sample-05/run.log

# Check delta log (each line is a JSON record)
tail -5 delta_log.jsonl | python3 -m json.tool

# Check source_b.csv
cat source_b.csv
```

## Real-world use cases

| Scenario | SOURCE_A | SOURCE_B | ID_COLUMN |
|----------|----------|----------|-----------|
| CRM export sync | crm_export.csv | local_contacts.csv | email |
| Order tracking | orders_master.csv | fulfilled_orders.csv | order_id |
| Employee list | hr_system.csv | badge_access.csv | employee_id |
| Inventory | warehouse.csv | store_stock.csv | sku |

# Cron Setup: File Drop Watcher & Processor

## Two deployment modes

### Mode A: Continuous watcher (recommended)
Run as a background process that watches indefinitely. Use `@reboot` cron or a systemd service.

### Mode B: Periodic batch (cron every N minutes)
Run on a schedule to process whatever is in input/ at that moment, then exit.

---

## Setup (both modes)

### 1. Create a virtual environment

```bash
cd /path/to/sample-03
python3 -m venv .venv
```

### 2. Install dependencies

```bash
.venv/bin/pip install -r requirements.txt
```

### 3. Create input/output/processed directories

```bash
mkdir -p input output processed
```

### 4. Configure your environment

```bash
cp .env.example .env
# Edit paths if needed
nano .env
```

### 5. Test a manual run

Create a test CSV:
```bash
cat > input/test_sales.csv << 'CSV'
date,product,quantity,price
2026-06-01,Widget A,10,25.50
2026-06-02,Widget B,5,49.99
2026-06-03,Widget A,8,25.50
CSV
```

Run the watcher:
```bash
bash run.sh
```

Press Ctrl+C to stop. Check output/:
```bash
ls output/
# processed_test_sales.csv

head output/processed_test_sales.csv
# date,product,quantity,price,__processed_at
# 2026-06-01,Widget A,10,25.50,2026-06-27 08:00:01
# ...
```

---

## Mode A: Start at system boot (crontab @reboot)

```bash
crontab -e
```

Add:
```
@reboot /path/to/sample-03/run.sh >> /path/to/sample-03/cron.log 2>&1
```

To start without rebooting:
```bash
nohup bash /path/to/sample-03/run.sh >> /path/to/sample-03/cron.log 2>&1 &
echo $! > /path/to/sample-03/watcher.pid
```

To stop:
```bash
kill $(cat /path/to/sample-03/watcher.pid)
```

---

## Mode B: Cron every 5 minutes (batch)

```bash
crontab -e
```

Add:
```
*/5 * * * * /path/to/sample-03/run.sh >> /path/to/sample-03/cron.log 2>&1
```

The script will process all CSVs in input/ then exit immediately (no blocking watch loop
when no files are present).

---

## Verify it ran

```bash
# Check run log
tail -30 /path/to/sample-03/run.log

# List processed files
ls -la output/
ls -la processed/
```

## Output file format

`output/processed_<original_name>.csv` is identical to the input CSV with one extra column:
- `__processed_at` -- ISO timestamp of when the file was processed

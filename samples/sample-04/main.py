"""
Sample 04 -- Scheduled Report Emailer
Reads a metrics CSV, builds an HTML email report, and sends it via SMTP
(Gmail app password). Designed to run weekly. Logs each send to sends.log.

Env vars: SMTP_USER, SMTP_PASS, REPORT_TO
"""

import os
import csv
import logging
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# -- Configuration (override via .env) ----------------------------------------
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
REPORT_TO = os.getenv("REPORT_TO", "")
REPORT_FROM = os.getenv("REPORT_FROM", SMTP_USER)
METRICS_CSV = os.getenv("METRICS_CSV", "metrics.csv")
LOG_FILE = os.getenv("LOG_FILE", "run.log")
SENDS_LOG = os.getenv("SENDS_LOG", "sends.log")

# -- Logging setup ------------------------------------------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# -- CSV helpers --------------------------------------------------------------

def load_metrics(csv_path):
    """
    Load all rows from the metrics CSV.
    Returns (fieldnames, rows) or raises if file is missing/empty.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError("Metrics CSV not found: {}".format(path))

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    if not rows:
        raise ValueError("Metrics CSV is empty: {}".format(path))

    return fieldnames, rows


def numeric_totals(rows, fieldnames):
    """Compute sum for numeric columns."""
    totals = {}
    for col in fieldnames:
        values = []
        for row in rows:
            try:
                values.append(float(row[col]))
            except (ValueError, TypeError):
                pass
        if values:
            totals[col] = sum(values)
    return totals


# -- Email builders -----------------------------------------------------------

def build_html_report(fieldnames, rows, totals, report_date):
    """Build an HTML email body from the metrics data."""
    # Build table rows
    table_rows_html = ""
    for i, row in enumerate(rows):
        bg = "#f9f9f9" if i % 2 == 0 else "#ffffff"
        cells = "".join(
            "<td style='padding:8px 12px;border-bottom:1px solid #eee;'>{}</td>".format(
                row.get(col, "")
            )
            for col in fieldnames
        )
        table_rows_html += "<tr style='background:{};'>{}</tr>".format(bg, cells)

    # Build totals row
    totals_cells = ""
    for col in fieldnames:
        if col in totals:
            totals_cells += (
                "<td style='padding:8px 12px;font-weight:bold;background:#e8f5e9;'>"
                "{:.2f}</td>".format(totals[col])
            )
        else:
            totals_cells += (
                "<td style='padding:8px 12px;font-weight:bold;background:#e8f5e9;'>"
                "—</td>"
            )

    # Build header row
    header_cells = "".join(
        "<th style='padding:10px 12px;background:#2e7d32;color:#fff;"
        "text-align:left;font-weight:600;'>{}</th>".format(col)
        for col in fieldnames
    )

    html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Weekly Metrics Report</title>
</head>
<body style="font-family:Arial,sans-serif;max-width:800px;margin:0 auto;padding:24px;color:#333;">

<div style="background:#2e7d32;color:#fff;padding:24px 32px;border-radius:8px 8px 0 0;">
  <h1 style="margin:0;font-size:22px;">Weekly Metrics Report</h1>
  <p style="margin:6px 0 0;opacity:0.85;font-size:14px;">Generated: {report_date}</p>
</div>

<div style="background:#fff;border:1px solid #e0e0e0;border-top:none;padding:24px;border-radius:0 0 8px 8px;">

  <h2 style="font-size:16px;color:#2e7d32;margin-top:0;">Summary</h2>
  <ul style="padding-left:20px;line-height:1.8;">
    <li>Total rows: <strong>{row_count}</strong></li>
    <li>Columns: <strong>{col_count}</strong></li>
    {totals_summary}
  </ul>

  <h2 style="font-size:16px;color:#2e7d32;">Data</h2>
  <div style="overflow-x:auto;">
  <table style="width:100%;border-collapse:collapse;font-size:14px;">
    <thead><tr>{header_cells}</tr></thead>
    <tbody>{table_rows}</tbody>
    <tfoot><tr>{totals_cells}</tr></tfoot>
  </table>
  </div>

  <p style="margin-top:24px;font-size:12px;color:#888;">
    This report was generated automatically by the Forgemind Course Automation Sample.
  </p>
</div>

</body>
</html>""".format(
        report_date=report_date,
        row_count=len(rows),
        col_count=len(fieldnames),
        totals_summary="".join(
            "<li>{}: <strong>{:.2f}</strong></li>".format(k, v)
            for k, v in totals.items()
        ),
        header_cells=header_cells,
        table_rows=table_rows_html,
        totals_cells=totals_cells,
    )
    return html


def build_text_report(fieldnames, rows, totals, report_date):
    """Build a plain-text fallback version of the report."""
    lines = [
        "Weekly Metrics Report",
        "Generated: {}".format(report_date),
        "",
        "SUMMARY",
        "  Rows    : {}".format(len(rows)),
        "  Columns : {}".format(len(fieldnames)),
    ]
    for col, total in totals.items():
        lines.append("  {} total: {:.2f}".format(col, total))
    lines.append("")
    lines.append("DATA")
    lines.append("  " + " | ".join(fieldnames))
    lines.append("  " + "-" * (len(" | ".join(fieldnames)) + 2))
    for row in rows:
        lines.append("  " + " | ".join(str(row.get(c, "")) for c in fieldnames))
    return "\n".join(lines)


# -- SMTP send ----------------------------------------------------------------

def send_email(subject, html_body, text_body, to_addr, from_addr, smtp_user, smtp_pass):
    """Send an HTML email with plain-text fallback via SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(from_addr, [to_addr], msg.as_string())


def log_send(sends_log_path, to_addr, subject, row_count, status):
    """Append a record to sends.log."""
    with open(sends_log_path, "a", encoding="utf-8") as f:
        f.write("{},{},{},{},{}\n".format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            to_addr,
            subject,
            row_count,
            status,
        ))


# -- Main ---------------------------------------------------------------------

def main():
    run_start = datetime.datetime.now()
    report_date = run_start.strftime("%Y-%m-%d %H:%M:%S")

    log.info("-" * 60)
    log.info("Run started | metrics=%s | to=%s", METRICS_CSV, REPORT_TO)

    # Validate config
    if not SMTP_USER:
        print("[ERROR] SMTP_USER not set. Copy .env.example to .env and configure.")
        log.error("SMTP_USER not set")
        return 1
    if not SMTP_PASS:
        print("[ERROR] SMTP_PASS not set.")
        log.error("SMTP_PASS not set")
        return 1
    if not REPORT_TO:
        print("[ERROR] REPORT_TO not set.")
        log.error("REPORT_TO not set")
        return 1

    # Load metrics
    try:
        fieldnames, rows = load_metrics(METRICS_CSV)
    except (FileNotFoundError, ValueError) as exc:
        log.error("Failed to load metrics: %s", exc)
        print("[ERROR] {}".format(exc))
        return 1

    totals = numeric_totals(rows, fieldnames)

    # Build email
    subject = "Weekly Metrics Report -- {}".format(
        run_start.strftime("%b %d, %Y")
    )
    html_body = build_html_report(fieldnames, rows, totals, report_date)
    text_body = build_text_report(fieldnames, rows, totals, report_date)

    # Send
    sends_log = Path(SENDS_LOG)
    if not sends_log.exists():
        with open(sends_log, "w") as f:
            f.write("sent_at,to,subject,row_count,status\n")

    try:
        send_email(subject, html_body, text_body, REPORT_TO, REPORT_FROM, SMTP_USER, SMTP_PASS)
        status = "OK"
        log.info("Email sent | to=%s | subject=%s | rows=%d", REPORT_TO, subject, len(rows))
    except smtplib.SMTPAuthenticationError as exc:
        status = "AUTH_ERROR"
        log.error("SMTP auth failed: %s", exc)
        print("[ERROR] SMTP authentication failed. Check SMTP_USER and SMTP_PASS.")
        log_send(sends_log, REPORT_TO, subject, len(rows), status)
        return 1
    except smtplib.SMTPException as exc:
        status = "SMTP_ERROR"
        log.error("SMTP error: %s", exc)
        print("[ERROR] SMTP error: {}".format(exc))
        log_send(sends_log, REPORT_TO, subject, len(rows), status)
        return 1
    except Exception as exc:
        status = "ERROR"
        log.error("Unexpected error: %s", exc)
        print("[ERROR] {}".format(exc))
        log_send(sends_log, REPORT_TO, subject, len(rows), status)
        return 1

    log_send(sends_log, REPORT_TO, subject, len(rows), status)

    elapsed = (datetime.datetime.now() - run_start).total_seconds()
    log.info("Run complete | elapsed=%.2fs", elapsed)

    print("\n" + "=" * 55)
    print("  Report Emailer -- Run Complete")
    print("=" * 55)
    print("  To       : {}".format(REPORT_TO))
    print("  Subject  : {}".format(subject))
    print("  Rows     : {}".format(len(rows)))
    print("  Columns  : {}".format(", ".join(fieldnames)))
    if totals:
        print("  Totals   :")
        for col, total in totals.items():
            print("    {} = {:.2f}".format(col, total))
    print("  Status   : {}".format(status))
    print("  Elapsed  : {:.2f}s".format(elapsed))
    print("  Sends log: {}".format(SENDS_LOG))
    print("=" * 55 + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

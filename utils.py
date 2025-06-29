# utils.py

from datetime import datetime

LOG_FILE = "report_log.txt"

def log_scan(entry):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{now}] {entry}\n")

def read_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No logs found."


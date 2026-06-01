import csv
import os

# Name of the main data file
DATA_FILE = "tasks_data.csv"

FIELDNAMES = [
    "task_id",
    "task_name",
    "assigned_to",
    "deadline",
    "status",
    "remarks",
]


def save_tasks(tasks: list) -> None:
    """Overwrite the CSV file with the current task list."""
    try:
        with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(tasks)
    except IOError as e:
        print(f"  [ERROR] Could not save data: {e}")


def load_tasks() -> list:
    """Load tasks from the CSV file. Returns [] if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]
    except IOError as e:
        print(f"  [ERROR] Could not load data: {e}")
        return []
    except Exception as e:
        print(f"  [ERROR] Unexpected error reading file: {e}")
        return []


def backup_tasks(tasks: list) -> None:
    """Save a timestamped backup copy of the task data."""
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"tasks_backup_{ts}.csv"
    try:
        with open(backup_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(tasks)
        print(f"  [✓] Backup saved: {backup_file}")
    except IOError as e:
        print(f"  [ERROR] Could not create backup: {e}")
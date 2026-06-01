from datetime import datetime

#  CONSTANTS
VALID_STATUSES = ["Not Started", "In Progress", "Completed", "Delayed", "Cancelled"]



DIVIDER  = "=" * 68
DIVIDER2 = "-" * 68

#  DISPLAY HELPERS
def print_header(title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {title.upper()}")
    print(DIVIDER)


def print_subheader(title: str) -> None:
    print(f"\n{DIVIDER2}")
    print(f"  {title}")
    print(DIVIDER2)

#  INPUT HELPERS
def get_nonempty_input(prompt: str) -> str:
    """Keep prompting until the user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  [!] This field cannot be empty. Please try again.")


def get_date_input(prompt: str, allow_empty: bool = False) -> str:
    """
    Prompt for a date in YYYY-MM-DD format.
    If allow_empty=True, pressing Enter returns an empty string.
    """
    while True:
        value = input(prompt).strip()
        if allow_empty and value == "":
            return ""
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("  [!] Invalid format. Please use YYYY-MM-DD  (e.g., 2025-07-20).")


def get_choice_input(prompt: str, choices: list) -> str:
    """Show a numbered list and return the user's selected value."""
    print(prompt)
    for i, choice in enumerate(choices, start=1):
        print(f"    [{i}] {choice}")
    while True:
        raw = input("  Enter number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1]
        print(f"  [!] Enter a number between 1 and {len(choices)}.")


def get_yes_no(prompt: str) -> bool:
    """Return True for yes, False for no."""
    while True:
        ans = input(f"{prompt} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("  [!] Please type 'y' or 'n'.")

#  ID GENERATION
def generate_id(tasks: list) -> str:
    """Generate the next Task ID in the format TASK-001, TASK-002, …"""
    if not tasks:
        return "TASK-001"
    nums = []
    for t in tasks:
        try:
            tid = t["task_id"]
            if tid.startswith("TASK-"):
                nums.append(int(tid.split("-")[1]))
        except (IndexError, ValueError):
            pass
    return f"TASK-{(max(nums) + 1 if nums else 1):03d}"


#  DEADLINE 
def days_remaining(deadline: str) -> str:
    """Return a human-readable deadline status string."""
    if not deadline:
        return "No deadline set"
    try:
        d = datetime.strptime(deadline, "%Y-%m-%d")
        diff = (d - datetime.today()).days
        if diff < 0:
            return f"OVERDUE by {abs(diff)} day(s)"
        elif diff == 0:
            return "Due TODAY"
        else:
            return f"{diff} day(s) remaining"
    except ValueError:
        return "Invalid date"

#  TASK CARD FORMATTER
def format_task_card(task: dict, index: int = None) -> str:
    """Return a formatted string that displays one task record."""
    prefix = f"[{index}] " if index is not None else "    "
    dl_note = days_remaining(task.get("deadline", ""))
    lines = [
        f"\n  {prefix}Task ID   : {task.get('task_id', 'N/A')}",
        f"      Task      : {task.get('task_name', 'N/A')}",
        f"      Assigned  : {task.get('assigned_to', 'N/A')}",
        f"      Deadline  : {task.get('deadline', 'N/A')}  ({dl_note})",
        f"      Status    : {task.get('status', 'N/A')}",
        f"      Remarks   : {task.get('remarks', 'None')}",
    ]
    return "\n".join(lines)
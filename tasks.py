from utils import (
    print_header,
    print_subheader,
    get_nonempty_input,
    get_date_input,
    get_choice_input,
    get_yes_no,
    generate_id,
    format_task_card,
    days_remaining,
    VALID_STATUSES,
    DIVIDER,
    DIVIDER2,
)
from file_handler import save_tasks


#  CREATE — Add a new task
def add_task(tasks: list) -> None:
    """Collect task details from the user and save a new record."""
    print_header("Add New Task")

    task_id = generate_id(tasks)
    print(f"  Auto-generated Task ID: {task_id}\n")

    task_name   = get_nonempty_input("  Task Name / Description : ")
    assigned_to = get_nonempty_input("  Assigned To (Name)      : ")
    deadline = get_date_input("\n  Deadline (YYYY-MM-DD)   : ")
    status      = get_choice_input("\n  Status:", VALID_STATUSES)
    remarks     = input("  Remarks / Updates       : ").strip()
    if not remarks:
        remarks = "None"

    new_task = {
        "task_id":     task_id,
        "task_name":   task_name,
        "assigned_to": assigned_to,
        "deadline":    deadline,
        "status":      status,
        "remarks":     remarks,
    }

    print_subheader("Preview")
    print(format_task_card(new_task))

    if get_yes_no("\n  Save this task?"):
        tasks.append(new_task)
        save_tasks(tasks)
        print(f"\n  [✓] Task '{task_id}' added successfully!")
    else:
        print("  [!] Task not saved.")

#  READ — View all tasks
def view_all_tasks(tasks: list) -> None:
    """Display every task in a formatted card layout."""
    print_header("All Tasks")

    if not tasks:
        print("  No tasks found. Add a task first.")
        return

    print(f"  Total tasks: {len(tasks)}\n")
    for i, task in enumerate(tasks, start=1):
        print(format_task_card(task, index=i))
        print(f"  {DIVIDER2}")


#  READ — View task by ID
def view_task_by_id(tasks: list) -> None:
    """Find and display a single task by its Task ID."""
    print_header("View Task by ID")

    if not tasks:
        print("  No tasks available.")
        return

    tid = get_nonempty_input("  Enter Task ID (e.g., TASK-001): ").upper()

    for task in tasks:
        if task["task_id"].upper() == tid:
            print(format_task_card(task))
            return

    print(f"  [!] No task found with ID '{tid}'.")

#  READ — Search tasks by keyword
def search_tasks(tasks: list) -> None:
    """Search across task name, assignee, status, and remarks."""
    print_header("Search Tasks")

    if not tasks:
        print("  No tasks available.")
        return

    keyword = get_nonempty_input("  Enter keyword to search: ").lower()

    results = [
        t for t in tasks
        if keyword in t["task_name"].lower()
        or keyword in t["assigned_to"].lower()
        or keyword in t["status"].lower()
        or keyword in t["remarks"].lower()
    ]

    if not results:
        print(f"  [!] No tasks matched '{keyword}'.")
        return

    print(f"\n  Found {len(results)} matching task(s):\n")
    for i, task in enumerate(results, start=1):
        print(format_task_card(task, index=i))
        print(f"  {DIVIDER2}")

#  READ — Filter by status
def filter_by_status(tasks: list) -> None:
    """Show only tasks that match a chosen status."""
    print_header("Filter Tasks by Status")

    if not tasks:
        print("  No tasks available.")
        return

    status = get_choice_input("  Select status to filter:", VALID_STATUSES)
    results = [t for t in tasks if t["status"] == status]

    if not results:
        print(f"  [!] No tasks with status '{status}'.")
        return

    print(f"\n  Tasks with status '{status}' ({len(results)} found):\n")
    for i, task in enumerate(results, start=1):
        print(format_task_card(task, index=i))
        print(f"  {DIVIDER2}")

#  READ — Filter by assignee
def filter_by_member(tasks: list) -> None:
    """Show only tasks assigned to a chosen group member role."""
    print_header("Filter Tasks by Assigned Member")

    if not tasks:
        print("  No tasks available.")
        return

    member = get_nonempty_input("  Enter member name to filter: ")
    results = [t for t in tasks if member.lower() in t["assigned_to"].lower()]

    if not results:
        print(f"  [!] No tasks assigned to '{member}'.")
        return

    print(f"\n  Tasks assigned to '{member}' ({len(results)} found):\n")
    for i, task in enumerate(results, start=1):
        print(format_task_card(task, index=i))
        print(f"  {DIVIDER2}")



#  UPDATE — Edit a task record
def update_task(tasks: list) -> None:
    """
    Locate a task by ID and let the user update any field.
    Pressing Enter on a field keeps the current value.
    """
    print_header("Update Task")

    if not tasks:
        print("  No tasks available to update.")
        return

    tid = get_nonempty_input("  Enter Task ID to update (e.g., TASK-001): ").upper()

    target = None
    target_idx = -1
    for i, task in enumerate(tasks):
        if task["task_id"].upper() == tid:
            target = task
            target_idx = i
            break

    if target is None:
        print(f"  [!] No task found with ID '{tid}'.")
        return

    print("\n  Current task details:")
    print(format_task_card(target))
    print("\n  (Press Enter to keep the current value.)\n")

    # Task name
    new_name = input(f"  New Task Name [{target['task_name']}]: ").strip()
    if new_name:
        target["task_name"] = new_name

    # Assigned to
    new_assigned = input(f"  New Assigned To [{target['assigned_to']}]: ").strip()
    if new_assigned:
        target["assigned_to"] = new_assigned

    # Deadline
    if get_yes_no("  Update Deadline?"):
        target["deadline"] = get_date_input("  New Deadline (YYYY-MM-DD): ")

    # Status
    if get_yes_no("  Update Status?"):
        target["status"] = get_choice_input("  Select new Status:", VALID_STATUSES)

    # Remarks
    new_remarks = input(f"  New Remarks [{target['remarks']}]: ").strip()
    if new_remarks:
        target["remarks"] = new_remarks

    print("\n  Updated task:")
    print(format_task_card(target))

    if get_yes_no("\n  Save these changes?"):
        tasks[target_idx] = target
        save_tasks(tasks)
        print(f"  [✓] Task '{tid}' updated successfully!")
    else:
        print("  [!] Changes discarded.")


#  DELETE — Remove a task
def delete_task(tasks: list) -> None:
    """Remove a task by ID after confirmation."""
    print_header("Delete Task")

    if not tasks:
        print("  No tasks available to delete.")
        return

    tid = get_nonempty_input("  Enter Task ID to delete (e.g., TASK-001): ").upper()

    target = None
    for task in tasks:
        if task["task_id"].upper() == tid:
            target = task
            break

    if target is None:
        print(f"  [!] No task found with ID '{tid}'.")
        return

    print("\n  Task to be deleted:")
    print(format_task_card(target))

    print("\n  [WARNING] This action cannot be undone.")
    if get_yes_no("  Confirm deletion?"):
        tasks.remove(target)
        save_tasks(tasks)
        print(f"  [✓] Task '{tid}' deleted.")
    else:
        print("  [!] Deletion cancelled.")


#  SUMMARY — Progress overview
def show_summary(tasks: list) -> None:
    """Display a statistics overview of all tasks."""
    print_header("Project Progress Summary")

    if not tasks:
        print("  No tasks on record.")
        return

    total = len(tasks)
    print(f"\n  Total Tasks: {total}\n")

    # Status breakdown with progress bar
    print("  ── Progress by Status ──────────────────────────────")
    for status in VALID_STATUSES:
        count = sum(1 for t in tasks if t["status"] == status)
        pct   = (count / total * 100) if total else 0
        bar   = "█" * count
        print(f"    {status:<14}: {bar:<15} {count} task(s)  ({pct:.0f}%)")

    # Per-member workload
    print("\n  ── Workload by Member ──────────────────────────────")
    unique_members = sorted(set(t["assigned_to"] for t in tasks if t["assigned_to"]))
    for member in unique_members:
        member_tasks = [t for t in tasks if t["assigned_to"] == member]
        done    = sum(1 for t in member_tasks if t["status"] == "Completed")
        pending = len(member_tasks) - done
        print(f"    {member:<20}: {len(member_tasks)} task(s) "
              f"[{done} done, {pending} pending]")

    # Overdue tasks
    from datetime import datetime
    overdue = [
        t for t in tasks
        if t["deadline"] and t["status"] != "Completed"
        and datetime.strptime(t["deadline"], "%Y-%m-%d") < datetime.today()
    ]
    if overdue:
        print(f"\n  ── Overdue Tasks ({len(overdue)}) ──────────────────────────")
        for t in overdue:
            print(f"    {t['task_id']}  {t['task_name']}  "
                  f"[{t['assigned_to']}] — {days_remaining(t['deadline'])}")
    else:
        print("\n  No overdue tasks. Great job!")

    print(f"\n  {DIVIDER}")
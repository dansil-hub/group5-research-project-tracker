# Research Project Tracker
### Mini Software Development Simulation — Python Final Project

---

## System Description

The **Research Project Tracker** is a Python-based desktop application designed to help a Researchers manage and monitor their project tasks from start to finish. It provides a clean graphical user interface (GUI) built with **tkinter** that allows team members to record tasks, assign responsibilities, set deadlines, track progress, and leave remarks or updates — all saved automatically to a file so no data is lost between sessions.


---

## Features (CRUD)

### CREATE
- **Add New Task** — Enter a task name, assign it to a team member, set a deadline using the year/month/day dropdowns, choose a status, and add remarks. A unique Task ID is automatically generated (TASK-001, TASK-002, etc.)

### READ
- **View All Tasks** — Displays all tasks in a color-coded table
- **Search Tasks** — Live search bar filters tasks by any keyword
- **Filter by Status** — Dropdown filter to show only tasks of a selected status
- **Project Progress Summary** — Popup showing task count by status, workload per member, and overdue tasks with progress bars

### UPDATE
- **Edit Task** — Double-click any row or click Edit Task to modify any field of an existing task. Changes are saved immediately.

### DELETE
- **Delete Task** — Select a task and click Delete Task. A confirmation dialog prevents accidental deletion.

### SYSTEM
- **Backup Data** — Creates a timestamped CSV backup copy of all task data

---

## Data Fields

| Field      | Description                                                 |
|-------------|------------------------------------------------------------|
| Task ID     | Auto-generated unique ID (e.g. TASK-001)                   |
| Task Name   | Description of the task                                    |
| Assigned To | Name of the team member responsible                        |
| Deadline    | Year / Month / Day selected from dropdowns                 |
| Status      | Not Started, In Progress, Completed, Delayed, or Cancelled |
| Remarks     | Updates, notes, or progress comments                       |

---

## Status Color Coding

| Status      | Color |
|-------------|-------|
| Not Started | Gray  |
| In Progress | Blue  |
| Completed   | Green |
| Delayed     | Red   |

---

## Instructions on How to Run the System

# Option one

### Requirements
- Python 3.6 or higher
- No external libraries required — uses built-in `tkinter` only

### File Structure
Make sure all these files are in the **same folder**:

```
Research Project Tracker/
├── main.py        ← Main GUI application (run this)
├── tasks.py           ← CRUD logic
├── file_handler.py    ← Save and load data (CSV)
├── utils.py           ← Validation and helper functions
└── tasks_data.csv     ← Auto-created on first save
```

### Steps to Run

**Step 1** — Open the project folder in VS Code

**Step 2** — Open the terminal in VS Code using:
```
Ctrl + `
```

**Step 3** — Run the program:
```bash
python main.py
```

**Step 4** — The application window will open. Use the sidebar buttons to manage tasks.

### Icon Images
To display images on the sidebar buttons, make sure the PNG files is in the same folder:
```
icon-add.png
icon-edit.png
icon-delete.png
icon-progress.png
icon-backup.png
```
If the files are missing, the buttons will still work — they just show text only.

# Option 2 (Easy)
No need for python
Download the dist file
  Double Click on main.exe
    IF encounter an windows protection warning, Run it as Administrator

---

## Group Members

| Name                     | Role            | Responsibilities                                                          |
|--------------------------|-----------------|---------------------------------------------------------------------------|
| (Montilla, Pelito R.)    | Project Manager | Defined project scope, assigned tasks, set deadlines, presents the system |
| (Tapitan, Dancelle L.)   | Developer 1     | Built main_gui.py and tasks.py — CRUD logic and GUI                       |
| (Teraza, John Patrick)   | Developer 2     | Built file_handler.py and utils.py — file saving and validation           |
| (Moscoso, Micho Elly B.) | Client          | Defined system requirements, validated features, suggested improvements   |
| (Tablon, Karl James )    | QA Specialist  
Ran all 21 test cases, documented results           |

---

## Exception Handling

| Scenario                         | How It Is Handled                                |
|----------------------------------|--------------------------------------------------|
| Empty Task Name                  | Warning dialog shown, form does not close        |
| Invalid date format              | Warning dialog shown with correct format example |
| No task selected for Edit/Delete | Info dialog prompts user to select a row first   |
| Missing data file                | System starts with an empty task list            |
| File save/load error             | Error message printed, system continues running  |

---

*Research Project Tracker — Python Final Project*
*Developed using Python tkinter — No external libraries required*

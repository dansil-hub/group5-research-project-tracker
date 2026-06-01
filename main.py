import os
import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

from file_handler import load_tasks, save_tasks, backup_tasks
from utils import generate_id, days_remaining, VALID_STATUSES

#  THEME COLORS
BG_DARK    = "#19142B"
BG_MAIN    = "#f4f6fb"
BG_CARD    = "#ffffff"
BG_HEADER  = "#2c3a5c"
ACCENT     = "#4f80e1"
ACCENT2    = "#6c47e8"
TEXT_LIGHT = "#ffffff"
TEXT_DARK  = "#1a1f2e"
TEXT_MUTED = "#8892a4"

STATUS_COLORS = {
    "Not Started": "#e0e0e0",
    "In Progress":  "#cce0ff",
    "Completed":    "#ccf0d4",
    "Delayed":      "#ffd6d6",
}
STATUS_FG = {
    "Not Started": "#555555",
    "In Progress":  "#1a4a8a",
    "Completed":    "#145a2e",
    "Delayed":      "#8a1a1a",
}


#  ADD / EDIT DIALOG
class TaskDialog(tk.Toplevel):
    def __init__(self, parent, task=None):
        super().__init__(parent)
        self.result = None
        self.task   = task
        self.title("Edit Task" if task else "Add New Task")
        self.resizable(False, False)
        self.configure(bg=BG_CARD)
        self.grab_set()
        self._build_ui()
        self._center()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr,
                 text="   Edit Task" if self.task else "  Add New Task",
                 font=("Mont", 13, "bold"),
                 bg=ACCENT, fg=TEXT_LIGHT).pack(side="left", padx=20, pady=14)

        form = tk.Frame(self, bg=BG_CARD, padx=28, pady=20)
        form.pack(fill="both", expand=True)

        def field(label, row):
            tk.Label(form, text=label, font=("Mont", 9, "bold"),
                     bg=BG_CARD, fg=TEXT_MUTED).grid(
                row=row, column=0, sticky="w", pady=(10, 2))

        field("TASK NAME / DESCRIPTION", 0)
        self.var_name = tk.StringVar(value=self.task["task_name"] if self.task else "")
        ttk.Entry(form, textvariable=self.var_name, width=44,
                  font=("Mont", 10)).grid(row=1, column=0, columnspan=2, sticky="ew", ipady=5)

        field("ASSIGNED TO", 2)
        self.var_assigned = tk.StringVar(value=self.task["assigned_to"] if self.task else "")
        ttk.Entry(form, textvariable=self.var_assigned,
                     font=("Mont", 10), width=42).grid(row=3, column=0, columnspan=2, sticky="ew", ipady=4)

        tk.Label(form, text="DEADLINE", font=("Mont", 9, "bold"),
         bg=BG_CARD, fg=TEXT_MUTED).grid(row=4, column=0, sticky="w", pady=(10, 2))

        # parse existing deadline if editing
        _existing = self.task["deadline"] if self.task and self.task["deadline"] else ""
        if "," in _existing:
            _parts = _existing.split(",")   # new comma format
        elif "-" in _existing:
            _parts = _existing.split("-")   # old dash format (backwards compatible)
        else:
            _parts = ["", "", ""]           # "No deadline yet" or empty
        _y = _parts[0] if len(_parts) > 0 else ""
        _m = _parts[1] if len(_parts) > 1 else ""
        _d = _parts[2] if len(_parts) > 2 else ""

        deadline_frame = tk.Frame(form, bg=BG_CARD)
        deadline_frame.grid(row=5, column=0, sticky="w")

        self.var_year  = tk.StringVar(value=_y)
        self.var_month = tk.StringVar(value=_m)
        self.var_day   = tk.StringVar(value=_d)

        years  = [""] + [str(y) for y in range(2026, 2031)]
        months = [""] + [f"{m:02d}" for m in range(1, 13)]
        days   = [""] + [f"{d:02d}" for d in range(1, 32)]

        ttk.Combobox(deadline_frame, textvariable=self.var_year,
                    values=years, state="readonly",
                    font=("Mont", 10), width=6).pack(side="left", padx=(0, 4))
        tk.Label(deadline_frame, text="Year",
                font=("Mont", 8), bg=BG_CARD, fg=TEXT_MUTED).pack(side="left", padx=(0, 10))

        ttk.Combobox(deadline_frame, textvariable=self.var_month,
                    values=months, state="readonly",
                    font=("Mont", 10), width=4).pack(side="left", padx=(0, 4))
        tk.Label(deadline_frame, text="Month",
                font=("Mont", 8), bg=BG_CARD, fg=TEXT_MUTED).pack(side="left", padx=(0, 10))

        ttk.Combobox(deadline_frame, textvariable=self.var_day,
                    values=days, state="readonly",
                    font=("Mont", 10), width=4).pack(side="left", padx=(0, 4))
        tk.Label(deadline_frame, text="Day",
                font=("Mont", 8), bg=BG_CARD, fg=TEXT_MUTED).pack(side="left")

        tk.Label(form, text="STATUS", font=("Mont", 9, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).grid(row=4, column=1, sticky="w", padx=(12, 0), pady=(10, 2))


        self.var_status = tk.StringVar(value=self.task["status"] if self.task else VALID_STATUSES[0])
        ttk.Combobox(form, textvariable=self.var_status,
                     values=VALID_STATUSES, state="readonly",
                     font=("Mont", 10), width=20).grid(row=5, column=1, sticky="w", padx=(12, 0), ipady=4)

        field("REMARKS / UPDATES", 6)
        self.txt_remarks = tk.Text(form, height=4, width=44,
                                   font=("Mont", 10), relief="solid", bd=1,
                                   wrap="word", padx=6, pady=6)
        self.txt_remarks.grid(row=7, column=0, columnspan=2, sticky="ew")
        if self.task:
            existing = self.task.get("remarks", "")
            if existing and existing != "None":
                self.txt_remarks.insert("1.0", existing)

        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        btn_row = tk.Frame(self, bg=BG_CARD, padx=28, pady=14)
        btn_row.pack(fill="x")
        tk.Button(btn_row, text="  Save Task  ",
                  font=("Mont", 10, "bold"),
                  bg=ACCENT, fg=TEXT_LIGHT,
                  relief="flat", cursor="hand2",
                  padx=18, pady=8,
                  command=self._on_save).pack(side="right", padx=(8, 0))
        tk.Button(btn_row, text="Cancel",
                  font=("Mont", 10),
                  bg="#e8eaf0", fg=TEXT_DARK,
                  relief="flat", cursor="hand2",
                  padx=18, pady=8,
                  command=self.destroy).pack(side="right")

    def _on_save(self):
        name     = self.var_name.get().strip()
        assigned = self.var_assigned.get().strip()
        y = self.var_year.get().strip()
        m = self.var_month.get().strip()
        d = self.var_day.get().strip()

        if not y and not m and not d:
            deadline = "No deadline yet"
        else:
            deadline = f"{y},{m},{d}"
        status   = self.var_status.get().strip()
        remarks  = self.txt_remarks.get("1.0", "end-1c").strip()

        if not name:
            messagebox.showwarning("Missing Field", "Task Name cannot be empty.", parent=self)
            return

        self.result = {
            "task_name":   name,
            "assigned_to": assigned,
            "deadline":    deadline,
            "status":      status,
            "remarks":     remarks if remarks else "None",
        }
        self.destroy()

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        px = self.master.winfo_rootx() + (self.master.winfo_width()  - w) // 2
        py = self.master.winfo_rooty() + (self.master.winfo_height() - h) // 2
        self.geometry(f"+{px}+{py}")



#  PROGRESS DIALOG
class ProgressDialog(tk.Toplevel):
    def __init__(self, parent, tasks):
        super().__init__(parent)
        self.title("Project Progress Summary")
        self.resizable(False, False)
        self.configure(bg=BG_CARD)
        self.grab_set()
        self._build(tasks)
        self._center(parent)

    def _build(self, tasks):
        hdr = tk.Frame(self, bg=ACCENT2, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📊  Project Progress Summary",
                 font=("Mont", 13, "bold"),
                 bg=ACCENT2, fg=TEXT_LIGHT).pack(side="left", padx=20, pady=14)

        body = tk.Frame(self, bg=BG_CARD, padx=28, pady=20)
        body.pack(fill="both", expand=True)

        total = len(tasks)
        tk.Label(body, text=f"Total Tasks: {total}",
                 font=("Mont", 12, "bold"),
                 bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(0, 14))

        tk.Label(body, text="BY STATUS", font=("Mont", 9, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")

        for status in VALID_STATUSES:
            count = sum(1 for t in tasks if t["status"] == status)
            pct   = int(count / total * 100) if total else 0
            row = tk.Frame(body, bg=BG_CARD)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{status:<16}", font=("Mont", 10),
                     bg=BG_CARD, fg=TEXT_DARK, width=16, anchor="w").pack(side="left")
            bar_bg = tk.Frame(row, bg="#e8eaf0", height=18, width=180)
            bar_bg.pack(side="left", padx=(4, 8))
            bar_bg.pack_propagate(False)
            if pct > 0:
                tk.Frame(bar_bg, bg=ACCENT, height=18,
                         width=max(4, int(180 * pct / 100))).place(x=0, y=0, relheight=1)
            tk.Label(row, text=f"{count} task(s)  ({pct}%)",
                     font=("Mont", 9), bg=BG_CARD, fg=TEXT_MUTED).pack(side="left")

        tk.Label(body, text="\nWORKLOAD BY MEMBER", font=("Mont", 9, "bold"),
                 bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")


        now = datetime.today()
        overdue = [t for t in tasks
                   if t["deadline"] and t["status"] != "Completed"
                   and _valid_date(t["deadline"])
                   and datetime.strptime(t["deadline"], "%Y-%m-%d") < now]
        if overdue:
            tk.Label(body, text=f"\n⚠  {len(overdue)} OVERDUE TASK(S)",
                     font=("Mont", 9, "bold"),
                     bg=BG_CARD, fg="#cc3333").pack(anchor="w")
            for t in overdue:
                tk.Label(body,
                         text=f"  • {t['task_id']}  {t['task_name']}  [{t['assigned_to']}]",
                         font=("Mont", 9), bg=BG_CARD, fg="#cc3333").pack(anchor="w")
        else:
            tk.Label(body, text="\n✅  No overdue tasks!",
                     font=("Mont", 9, "bold"),
                     bg=BG_CARD, fg="#2e7d52").pack(anchor="w")

        tk.Button(body, text="Close", font=("Mont", 10),
                  bg="#e8eaf0", fg=TEXT_DARK, relief="flat",
                  cursor="hand2", padx=18, pady=6,
                  command=self.destroy).pack(anchor="e", pady=(20, 0))

    def _center(self, parent):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        px = parent.winfo_rootx() + (parent.winfo_width()  - w) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"+{px}+{py}")


def _valid_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False



#  HELPER — load a PNG image safely (falls back to None)
def _load_icon(filename):
    """
    Load a PNG file from the same folder as this script.
    Returns a PhotoImage on success, or None if the file is missing.
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        img = tk.PhotoImage(file=path)
        # subsample to shrink to roughly 20x20
        img = img.subsample(2, 2)
        return img
    except Exception:
        return None


#  MAIN APPLICATION WINDOW
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Research Project Tracker")
        self.geometry("1060x640")
        self.minsize(860, 520)
        self.configure(bg=BG_DARK)

        self.tasks = load_tasks()
        self._style()
        self._build_ui()
        self._populate()

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview",
                    font=("Mont", 10), rowheight=34,
                    background=BG_CARD, fieldbackground=BG_CARD, borderwidth=0)
        s.configure("Treeview.Heading",
                    font=("Mont", 9, "bold"),
                    background=BG_HEADER, foreground=TEXT_LIGHT,
                    relief="flat", padding=(10, 8))
        s.map("Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", TEXT_LIGHT)])
        s.configure("Vertical.TScrollbar",
                    background="#d0d4de", troughcolor=BG_MAIN,
                    borderwidth=0, arrowsize=14)
        s.configure("TEntry", fieldbackground=BG_CARD, relief="solid")
        s.configure("TCombobox", fieldbackground=BG_CARD)

    def _build_ui(self):
        # ─ Sidebar ──────────────────────────────────────────
        sidebar = tk.Frame(self, bg=BG_DARK, width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo area
        logo_frame = tk.Frame(sidebar, bg=BG_DARK, pady=28)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="📋", font=("Mont", 26),
                 bg=BG_DARK, fg=ACCENT).pack()
        tk.Label(logo_frame, text="Project\nTracker",
                 font=("Mont", 11, "bold"),
                 bg=BG_DARK, fg=TEXT_LIGHT, justify="center").pack(pady=(4, 0))

        tk.Frame(sidebar, bg="#2c3248", height=1).pack(fill="x", padx=18)

    
        self._icons = {
            "add":      _load_icon("icon-add.png"),
            "edit":     _load_icon("icon-edit.png"),
            "delete":   _load_icon("icon-delete.png"),
            "progress": _load_icon("icon-progress.png"),
            "backup":   _load_icon("icon-backup.png"),
        }

        # ── Button definitions ─────────────────────────────────────────
        # (label text,  command,          bg color,    icon key)
        btn_defs = [
            ("  Add Task",     self.cmd_add,     ACCENT,      "add"),
            ("  Edit Task",    self.cmd_edit,    "#3a3f58",   "edit"),
            ("  Delete Task",  self.cmd_delete,  "#3a3f58",   "delete"),
            ("  Progress",     self.cmd_summary, "#3a3f58",   "progress"),
            ("  Backup Data",  self.cmd_backup,  "#3a3f58",   "backup"),
        ]

        for text, cmd, color, icon_key in btn_defs:
            icon = self._icons.get(icon_key)
            b = tk.Button(sidebar,
                          text=text,
                          image=icon if icon else "",
                          compound="left",        # image on left, text on right
                          font=("Mont", 10),
                          bg=color, fg=TEXT_LIGHT,
                          relief="flat", cursor="hand2",
                          anchor="w", padx=14, pady=10,
                          bd=0, highlightthickness=0,
                          activebackground=ACCENT,
                          activeforeground=TEXT_LIGHT,
                          command=cmd)
            b.pack(fill="x", padx=10, pady=3)

        self.lbl_count = tk.Label(sidebar, text="0 tasks",
                                  font=("Mont", 9),
                                  bg=BG_DARK, fg=TEXT_MUTED)
        self.lbl_count.pack(side="bottom", pady=18)

        # ─ Main area ────────────────────────────────────────
        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(side="right", fill="both", expand=True)

        topbar = tk.Frame(main, bg=BG_MAIN, pady=14, padx=20)
        topbar.pack(fill="x")

        tk.Label(topbar, text="Task Board",
                 font=("Mont", 16, "bold"),
                 bg=BG_MAIN, fg=TEXT_DARK).pack(side="left")

        self.var_filter = tk.StringVar(value="All Status")
        filter_opts = ["All Status"] + VALID_STATUSES
        filter_cb = ttk.Combobox(topbar, textvariable=self.var_filter,
                                 values=filter_opts, state="readonly",
                                 font=("Mont", 9), width=16)
        filter_cb.pack(side="right", padx=(8, 0))
        filter_cb.bind("<<ComboboxSelected>>", lambda e: self._populate())

        tk.Label(topbar, text="Filter:",
                 font=("Mont", 9), bg=BG_MAIN, fg=TEXT_MUTED).pack(side="right")

        self.var_search = tk.StringVar()
        self.var_search.trace_add("write", lambda *a: self._populate())
        ttk.Entry(topbar, textvariable=self.var_search,
                  font=("Mont", 10), width=24).pack(side="right", padx=(8, 16), ipady=4)
        tk.Label(topbar, text="🔍 Search:",
                 font=("Mont", 9), bg=BG_MAIN, fg=TEXT_MUTED).pack(side="right")

        table_frame = tk.Frame(main, bg=BG_MAIN, padx=20)
        table_frame.pack(fill="both", expand=True)

        columns = ("task_id", "task_name", "assigned_to", "deadline", "status", "remarks")
        self.tree = ttk.Treeview(table_frame, columns=columns,
                                 show="headings", selectmode="browse")

        col_cfg = [
            ("task_id",     "Task No.",    80,  False),
            ("task_name",   "Task Name",  240,  False),
            ("assigned_to", "Assigned To",150,  False),
            ("deadline",    "Deadline",   110,  False),
            ("status",      "Status",     120,  False),
            ("remarks",     "Remarks",    200,  True),
        ]
        for col, heading, width, stretch in col_cfg:
            self.tree.heading(col, text=heading, command=lambda c=col: self._sort(c))
            self.tree.column(col, width=width, stretch=stretch, anchor="w", minwidth=60)

        for status, bg in STATUS_COLORS.items():
            self.tree.tag_configure(status, background=bg,
                                    foreground=STATUS_FG.get(status, TEXT_DARK))

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", lambda e: self.cmd_edit())

        self.statusbar = tk.Label(main, text="Ready",
                                  font=("Mont", 9),
                                  bg="#dde1ec", fg=TEXT_MUTED,
                                  anchor="w", padx=16, pady=6)
        self.statusbar.pack(fill="x", side="bottom")

        self._sort_col = None
        self._sort_rev = False

    def _populate(self):
        keyword = self.var_search.get().strip().lower()
        filt    = self.var_filter.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        shown = 0
        for t in self.tasks:
            if filt != "All Status" and t["status"] != filt:
                continue
            if keyword and not any(keyword in str(v).lower() for v in t.values()):
                continue
            dl = t.get("deadline", "")
            if not dl or dl == "No deadline yet":
                dl_display = "No deadline yet"
            elif "," in dl:
                y, m, d = (dl.split(",") + ["", "", ""])[:3]
                if y and m and d:
                    dl_display = f"{y}-{m}-{d}"
                else:
                    dl_display = f"{y if y else '-'}-{m if m else '-'}-{d if d else '-'}"
            else:
                dl_display = dl   # fallback for old saved data
            self.tree.insert("", "end", iid=t["task_id"],
                             values=(t["task_id"], t["task_name"], t["assigned_to"],
                                     dl_display, t["status"], t["remarks"]),
                             tags=(t["status"],))
            shown += 1

        total = len(self.tasks)
        self.lbl_count.config(text=f"{total} task(s) total")
        self.statusbar.config(
            text=f"Showing {shown} of {total} task(s)"
                 + (f'  ·  filter: {filt}' if filt != 'All Status' else "")
                 + (f'  ·  search: "{keyword}"' if keyword else ""))

    def _selected_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("No Selection", "Please select a task first.")
            return None
        tid = sel[0]
        for t in self.tasks:
            if t["task_id"] == tid:
                return t
        return None

    def _sort(self, col):
        if self._sort_col == col:
            self._sort_rev = not self._sort_rev
        else:
            self._sort_col = col
            self._sort_rev = False
        self.tasks.sort(key=lambda t: t.get(col, "").lower(), reverse=self._sort_rev)
        self._populate()

    def cmd_add(self):
        dlg = TaskDialog(self)
        self.wait_window(dlg)
        if dlg.result:
            task_id = generate_id(self.tasks)
            self.tasks.append({"task_id": task_id, **dlg.result})
            save_tasks(self.tasks)
            self._populate()
            self.tree.selection_set(task_id)
            self.tree.see(task_id)
            self.statusbar.config(text=f"✓  Task '{task_id}' added successfully.")

    def cmd_edit(self):
        task = self._selected_task()
        if not task:
            return
        dlg = TaskDialog(self, task=task)
        self.wait_window(dlg)
        if dlg.result:
            task.update(dlg.result)
            save_tasks(self.tasks)
            self._populate()
            self.tree.selection_set(task["task_id"])
            self.statusbar.config(text=f"✓  Task '{task['task_id']}' updated.")

    def cmd_delete(self):
        task = self._selected_task()
        if not task:
            return
        if messagebox.askyesno("Confirm Delete",
                               f"Delete task '{task['task_id']} – {task['task_name']}'?\n\nThis cannot be undone."):
            self.tasks.remove(task)
            save_tasks(self.tasks)
            self._populate()
            self.statusbar.config(text=f"✓  Task '{task['task_id']}' deleted.")

    def cmd_summary(self):
        ProgressDialog(self, self.tasks)

    def cmd_backup(self):
        backup_tasks(self.tasks)
        messagebox.showinfo("Backup", "Data backed up successfully!")
        self.statusbar.config(text="✓  Backup created.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
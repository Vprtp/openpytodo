import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Toplevel
import pickle
import os
from datetime import datetime

VERSION = "1.0.0"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"To Do - version {VERSION}")
        self.root.geometry("700x500")

        # Set window icon
        try:
            if os.name == "nt":
                self.root.iconbitmap('icon.ico')
            else:
                self.root.iconphoto(True, tk.PhotoImage(file='icon.png'))
        except Exception as e:
            print(f"Icon not found or couldn't be loaded: {e}")

        self.project_lists = {}
        self.current_project = None
        self.is_saved = True

        # Create the "data" directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')

        # Use ttk for modern widgets
        style = ttk.Style()
        style.theme_use("clam")

        # Adjusting the Treeview row height by increasing the padding and font size
        style.configure("Treeview", rowheight=50, font=('Arial', 12))

        # Scrollbar
        self.tree_scrollbar = ttk.Scrollbar(self.root)
        self.tree_scrollbar.grid(row=0, column=3, sticky="ns")
        
        # Task list with importance and date
        self.tree = ttk.Treeview(self.root, columns=("Importance", "Task", "Date"), show="headings", height=15, yscrollcommand=self.tree_scrollbar.set)
        self.tree.heading("Importance", text="Importance")
        self.tree.heading("Task", text="Task")
        self.tree.heading("Date", text="Date Added")
        self.tree.column("Importance", width=100, anchor="center")
        self.tree.column("Task", width=350, anchor="w")
        self.tree.column("Date", width=170, anchor="center")
        self.tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Configure the scrollbar
        self.tree_scrollbar.config(command=self.tree.yview)

        # Bind double-click event
        self.tree.bind("<Double-1>", self.show_full_task)

        # Task entry
        self.entry = ttk.Entry(self.root, font=('Arial', 12))
        self.entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Importance dropdown
        self.importance_var = tk.StringVar()
        self.importance_combobox = ttk.Combobox(self.root, textvariable=self.importance_var, state="readonly")
        self.importance_combobox['values'] = ("Normal", "Important", "Very Important")
        self.importance_combobox.current(0)
        self.importance_combobox.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Buttons
        self.add_button = ttk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=2, column=0, padx=10, pady=5)

        self.delete_button = ttk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=1, padx=10, pady=5)

        self.load_button = ttk.Button(self.root, text="Load Project", command=self.load_project)
        self.load_button.grid(row=3, column=0, padx=10, pady=5)

        self.new_button = ttk.Button(self.root, text="New Project", command=self.new_project)
        self.new_button.grid(row=3, column=1, padx=10, pady=5)

        self.save_button = ttk.Button(self.root, text="Save Project", command=self.save_project)
        self.save_button.grid(row=2, column=2, padx=10, pady=5)

        self.quit_button = ttk.Button(self.root, text="Quit", command=self.quit_program)
        self.quit_button.grid(row=3, column=2, padx=10, pady=5)

        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.load_projects()

        # Bind the close window event
        self.root.protocol("WM_DELETE_WINDOW", self.quit_program)

    def mark_unsaved(self):
        """Mark the project as unsaved."""
        if self.is_saved:
            self.is_saved = False
            self.root.title(f"To Do* - version {VERSION}")

    def mark_saved(self):
        """Mark the project as saved."""
        self.is_saved = True
        self.root.title(f"To Do - version {VERSION}")

    def add_task(self):
        task = self.entry.get()
        importance = self.importance_var.get()
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if task and self.current_project:
            self.project_lists[self.current_project].append((importance, task, date_added))
            self.entry.delete(0, tk.END)
            self.update_listbox()
            self.mark_unsaved()
        else:
            messagebox.showwarning("No Project Loaded", "Please load or create a project first.")

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item and self.current_project:
            task = self.tree.item(selected_item)['values'][1]
            self.project_lists[self.current_project] = [
                (importance, t, date) for (importance, t, date) in self.project_lists[self.current_project] if t != task
            ]
            self.update_listbox()
            self.mark_unsaved()
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to delete.")

    def load_project(self):
        projects = list(self.project_lists.keys())
        if projects:
            self.project_selection_window(projects)
        else:
            messagebox.showinfo("No Projects", "No projects found. Create a new project first.")

    def project_selection_window(self, projects):
        top = Toplevel(self.root)
        top.title("Select a Project")
        top.geometry("300x300")

        listbox = tk.Listbox(top)
        listbox.pack(fill=tk.BOTH, expand=True)

        for project in projects:
            listbox.insert(tk.END, project)

        def on_select():
            selected_project = listbox.get(listbox.curselection())
            self.current_project = selected_project
            self.update_listbox()
            self.mark_saved()
            top.destroy()

        select_button = ttk.Button(top, text="Load Project", command=on_select)
        select_button.pack(pady=10)

    def new_project(self):
        project_name = simpledialog.askstring("New Project", "Enter new project name:")
        if project_name:
            if project_name in self.project_lists:
                messagebox.showerror("Error", "Project already exists.")
            else:
                self.project_lists[project_name] = []
                self.current_project = project_name
                self.update_listbox()
                self.mark_unsaved()

    def save_project(self):
        if self.current_project:
            filepath = os.path.join('data', f'{self.current_project}.pkl')
            with open(filepath, 'wb') as file:
                pickle.dump(self.project_lists[self.current_project], file)
            self.mark_saved()
            messagebox.showinfo("Saved", f"Project '{self.current_project}' saved successfully.")
        else:
            messagebox.showwarning("No Project Loaded", "Please load or create a project first.")

    def load_projects(self):
        for filename in os.listdir('data'):
            if filename.endswith('.pkl'):
                project_name = filename[:-4]
                filepath = os.path.join('data', filename)
                with open(filepath, 'rb') as file:
                    self.project_lists[project_name] = pickle.load(file)

    def update_listbox(self):
        global tasks
        self.tree.delete(*self.tree.get_children())
        if self.current_project:
            tasks = sorted(self.project_lists[self.current_project], key=lambda x: self.get_importance_rank(x[0]))
            for importance, task, date in tasks:
                shortened_task = self.shorten_text(task, width=50)
                color = self.get_color(importance)
                self.tree.insert("", tk.END, values=(importance, shortened_task, date), tags=(color,))
            self.tree.tag_configure("blue", foreground="darkblue")
            self.tree.tag_configure("yellow", foreground="darkgoldenrod")
            self.tree.tag_configure("red", foreground="darkred")

    def shorten_text(self, text, width):
        if len(text) > width:
            return text[:width] + "..."
        return text

    def show_full_task(self, event):
        item = self.tree.selection()
        if item:
            task = tasks[int(item[0][1:])-1][1]
            messagebox.showinfo("Task Details", task)

    def get_importance_rank(self, importance):
        if importance == "Very Important":
            return 1
        elif importance == "Important":
            return 2
        else:
            return 3

    def get_color(self, importance):
        if importance == "Very Important":
            return "red"
        elif importance == "Important":
            return "yellow"
        else:
            return "blue"

    def quit_program(self):
        if not self.is_saved:
            if messagebox.askyesno("Quit", "You have unsaved changes. Do you really want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

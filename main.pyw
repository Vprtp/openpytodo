import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Toplevel
import pickle
import os
from datetime import datetime

VERSION = "1.0.1"

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
        self.save_button.grid(row=4, column=0, padx=10, pady=5)

        self.quit_button = ttk.Button(self.root, text="Quit", command=self.quit_program)
        self.quit_button.grid(row=4, column=2, padx=10, pady=5)

        self.edit_button = ttk.Button(self.root, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=2, column=2, padx=10, pady=5)

        self.delete_project_button = ttk.Button(self.root, text="Delete Project", command=self.delete_project)
        self.delete_project_button.grid(row=4, column=1, padx=10, pady=5)

        self.edit_project_button = ttk.Button(self.root, text="Edit Project", command=self.edit_project_name)
        self.edit_project_button.grid(row=3, column=2, padx=10, pady=5)

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
        elif self.current_project:
            messagebox.showwarning("Missing Task Parameters", "Please fill the necessary task parameters to add a task.")
        else:
            messagebox.showwarning("No Project Loaded", "Please load or create a project first.")

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item and self.current_project:
            task_index = int(selected_item[0])  # Retrieve the original index from the iid
            del self.project_lists[self.current_project][task_index]  # Delete the task from the list
            self.update_listbox()  # Refresh the listbox
            self.mark_unsaved()
        else:
            messagebox.showwarning("No Task Selected", "Please select a task to delete.")

    def edit_task(self):
        selected_item = self.tree.selection()
        if selected_item and self.current_project:
            task_index = int(selected_item[0])  # Retrieve the original index from the iid
            task_data = self.project_lists[self.current_project][task_index]
            original_importance, original_task, original_date = task_data

            # Create the top-level window for editing the task
            top = Toplevel(self.root)
            top.title("Edit Task")
            top.geometry("350x170")

            # Task Label and Entry for editing the task text
            ttk.Label(top, text="Task:").pack(pady=5)
            task_entry = ttk.Entry(top, width=50)
            task_entry.pack(pady=5)
            task_entry.insert(0, original_task)  # Pre-fill with the current task text

            # Importance Label and Combobox for editing the task importance
            ttk.Label(top, text="Importance:").pack(pady=5)
            importance_var = tk.StringVar()
            importance_combobox = ttk.Combobox(top, textvariable=importance_var, state="readonly")
            importance_combobox['values'] = ("Normal", "Important", "Very Important")
            importance_combobox.set(original_importance)  # Pre-select the current importance
            importance_combobox.pack(pady=5)

            # Function to save changes
            def save_changes():
                new_task = task_entry.get()
                if importance_combobox.get() != "":
                    new_importance = importance_combobox.get()
                else:
                    new_importance = original_importance

                if new_task:  # Ensure the task text is not empty
                    self.project_lists[self.current_project][task_index] = (new_importance, new_task, original_date)
                    self.update_listbox()  # Refresh the listbox with updated info
                    self.mark_unsaved()
                    top.destroy()  # Close the edit window
                else:
                    messagebox.showwarning("Input Error", "Task text cannot be empty.")

            # Save Button
            save_button = ttk.Button(top, text="Save Changes", command=save_changes)
            save_button.pack(pady=10)

        else:
            messagebox.showwarning("No Task Selected", "Please select a task to edit.")

    def load_project(self):
        # Check if there are unsaved changes by checking the window title for "*"
        if "*" in self.root.title():
            result = messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Do you want to continue and discard changes?")
            if not result:
                return  # Cancel loading if the user chooses 'No'
        
        # Proceed with project loading if no unsaved changes or user chooses 'Yes'
        projects = list(self.project_lists.keys())
        if projects:
            self.project_selection_window(projects)
        else:
            messagebox.showinfo("No Projects", "No projects found. Create a new project first.")

    def delete_project(self):
        if self.current_project:
            result = messagebox.askyesno("Delete Project", f"Are you sure you want to delete the project '{self.current_project}'?")
            if result:
                project_name = self.current_project  # Store the name before deletion
                del self.project_lists[self.current_project]  # Remove project from the dictionary
                
                # Delete the corresponding file
                filepath = os.path.join('data', f'{project_name}.pkl')
                if os.path.exists(filepath):
                    os.remove(filepath)
                    
                self.current_project = None  # Clear current project
                self.update_listbox()  # Refresh the task list
                self.mark_saved()  # Mark as saved, since we deleted the project
                messagebox.showinfo("Deleted", f"Project '{project_name}' deleted successfully.")  # Use stored name
        else:
            messagebox.showwarning("No Project Selected", "Please load or create a project first.")

    def edit_project_name(self):
        if self.current_project:
            new_project_name = simpledialog.askstring("Edit Project Name", "Enter new project name:", initialvalue=self.current_project)
            if new_project_name:
                if new_project_name in self.project_lists:
                    messagebox.showerror("Error", "Project with this name already exists.")
                else:
                    # Update the project name in the dictionary
                    self.project_lists[new_project_name] = self.project_lists.pop(self.current_project)  # Rename project

                    # Update the file names as well
                    old_filepath = os.path.join('data', f'{self.current_project}.pkl')
                    new_filepath = os.path.join('data', f'{new_project_name}.pkl')

                    # Rename the project file
                    if os.path.exists(old_filepath):
                        os.rename(old_filepath, new_filepath)

                    self.current_project = new_project_name
                    self.update_listbox()  # Refresh the task list
                    self.mark_unsaved()  # Mark as unsaved since we changed the project name
                    messagebox.showinfo("Success", f"Project renamed to '{new_project_name}'.")
        else:
            messagebox.showwarning("No Project Selected", "Please load or create a project first.")

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
            if selected_project == self.current_project:
                # Load project from disk only if it's not the currently loaded project
                result = messagebox.askyesno("Reload Project", "This project is already open. Do you want to reload it from disk?")
                if result:
                    self.load_project_from_file(selected_project)
            else:
                self.load_project_from_file(selected_project)

            top.destroy()

        select_button = ttk.Button(top, text="Load Project", command=on_select)
        select_button.pack(pady=10)

    def load_project_from_file(self, project_name):
        """Load the selected project and refresh the task list."""
        filepath = os.path.join('data', f'{project_name}.pkl')
        if os.path.exists(filepath):
            with open(filepath, 'rb') as file:
                # Load the project from the file, resetting any in-memory changes
                self.project_lists[project_name] = pickle.load(file)
            self.current_project = project_name
            self.update_listbox()
            self.mark_saved()  # Mark the project as saved, since we just loaded it from disk
        else:
            messagebox.showerror("Error", f"Project file for '{project_name}' not found.")


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
            # Prompt user only if there are unsaved changes
            if not self.is_saved:
                filepath = os.path.join('data', f'{self.current_project}.pkl')
                with open(filepath, 'wb') as file:
                    pickle.dump(self.project_lists[self.current_project], file)
                self.mark_saved()  # Mark the project as saved
                messagebox.showinfo("Saved", f"Project '{self.current_project}' saved successfully.")
            else:
                messagebox.showinfo("No Changes", "There are no changes to save.")
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
        self.tree.delete(*self.tree.get_children())  # Clear the current tasks in the tree
        if self.current_project:
            # Retrieve the unsorted tasks list
            original_tasks = self.project_lists[self.current_project]
            # Sort the tasks by importance for display
            tasks = sorted(enumerate(original_tasks), key=lambda x: self.get_importance_rank(x[1][0]))

            for index, (original_index, (importance, task, date)) in enumerate(tasks):
                shortened_task = self.shorten_text(task, width=50)  # Shorten the text for display
                color = self.get_color(importance)
                # Use the original index in the project list as the iid, so we can track it even after sorting
                self.tree.insert("", tk.END, iid=original_index, values=(importance, shortened_task, date), tags=(color,))
            
            # Configure the tree's tag colors
            self.tree.tag_configure("blue", foreground="darkblue")
            self.tree.tag_configure("yellow", foreground="darkgoldenrod")
            self.tree.tag_configure("red", foreground="darkred")

    def shorten_text(self, text, width):
        if len(text) > width:
            return text[:width] + "..."
        return text

    def show_full_task(self, event):
        selected_item = self.tree.selection()  # Get the selected item
        if selected_item:
            task_index = int(selected_item[0])  # Retrieve the original index from the iid
            task = self.project_lists[self.current_project][task_index][1]  # Get the full task text
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

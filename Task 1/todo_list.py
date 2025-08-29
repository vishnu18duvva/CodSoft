import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
from datetime import datetime
import json

DATA_FILE = Path.home() / "todo_data.json"

class TodoItem:
    def __init__(self, text, created=None, done=False):
        self.text = text
        self.created = created or datetime.now().isoformat()
        self.done = done

    def to_dict(self):
        return {"text": self.text, "created": self.created, "done": self.done}

    @staticmethod
    def from_dict(d):
        return TodoItem(d["text"], d.get("created"), d.get("done", False))

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")
        master.geometry("600x400")

        top = tk.Frame(master)
        top.pack(fill=tk.X, padx=8, pady=6)

        self.entry = tk.Entry(top)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,6))
        self.entry.bind('<Return>', lambda e: self.add_item())

        add_btn = tk.Button(top, text="Add", width=10, command=self.add_item)
        add_btn.pack(side=tk.LEFT)

        search_label = tk.Label(top, text="Search:")
        search_label.pack(side=tk.LEFT, padx=(8,4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.refresh_list)
        search_entry = tk.Entry(top, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT)

        middle = tk.Frame(master)
        middle.pack(fill=tk.BOTH, expand=True, padx=8)

        self.listbox = tk.Listbox(middle, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-1>', lambda e: self.toggle_done())

        scrollbar = tk.Scrollbar(middle, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        right = tk.Frame(master)
        right.pack(fill=tk.X, padx=8, pady=6)

        edit_btn = tk.Button(right, text="Edit", width=12, command=self.edit_item)
        edit_btn.pack(side=tk.LEFT, padx=(0,6))

        del_btn = tk.Button(right, text="Delete", width=12, command=self.delete_item)
        del_btn.pack(side=tk.LEFT, padx=(0,6))

        done_btn = tk.Button(right, text="Mark Done/Undone", width=16, command=self.toggle_done)
        done_btn.pack(side=tk.LEFT, padx=(0,6))

        save_btn = tk.Button(right, text="Save", width=10, command=self.save_data)
        save_btn.pack(side=tk.RIGHT, padx=(6,0))

        load_btn = tk.Button(right, text="Load", width=10, command=self.load_data)
        load_btn.pack(side=tk.RIGHT)

        clear_btn = tk.Button(master, text="Clear All", command=self.clear_all)
        clear_btn.pack(side=tk.BOTTOM, pady=(0,8))

        self.items = []  
        self.load_data()
        self.refresh_list()

    def add_item(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Empty", "Please enter a task.")
            return
        self.items.append(TodoItem(text))
        self.entry.delete(0, tk.END)
        self.refresh_list()

    def edit_item(self):
        idx = self._get_selected_index()
        if idx is None:
            return
        item = self.items[idx]
        new_text = simpledialog.askstring("Edit task", "Update task:", initialvalue=item.text)
        if new_text is None:
            return
        new_text = new_text.strip()
        if not new_text:
            messagebox.showwarning("Empty", "Task can't be empty")
            return
        item.text = new_text
        self.refresh_list()

    def delete_item(self):
        idx = self._get_selected_index()
        if idx is None:
            return
        confirm = messagebox.askyesno("Delete", "Delete selected task?")
        if not confirm:
            return
        self.items.pop(idx)
        self.refresh_list()

    def toggle_done(self):
        idx = self._get_selected_index()
        if idx is None:
            return
        self.items[idx].done = not self.items[idx].done
        self.refresh_list()

    def clear_all(self):
        if not self.items:
            return
        if messagebox.askyesno("Clear all", "Remove all tasks?"):
            self.items.clear()
            self.refresh_list()

    def save_data(self):
        try:
            data = [it.to_dict() for it in self.items]
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", f"Saved {len(self.items)} tasks to {DATA_FILE}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save: {e}")

    def load_data(self):
        if not DATA_FILE.exists():
            return
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.items = [TodoItem.from_dict(d) for d in data]
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data: {e}")

    def refresh_list(self, *args):
        search = self.search_var.get().lower().strip() if hasattr(self, 'search_var') else ''
        self.listbox.delete(0, tk.END)
        for i, item in enumerate(self.items):
            text = item.text
            if search and search not in text.lower():
                continue
            prefix = "[x] " if item.done else "[ ] "
            display = f"{prefix}{text}  (created: {item.created.split('T')[0]})"
            self.listbox.insert(tk.END, display)

    def _get_selected_index(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Select", "Please select a task first")
            return None
        selected_text = self.listbox.get(sel[0])
        for i, item in enumerate(self.items):
            prefix = "[x] " if item.done else "[ ] "
            candidate = f"{prefix}{item.text}  (created: {item.created.split('T')[0]})"
            if candidate == selected_text:
                return i
        return None

if __name__ == '__main__':
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
    

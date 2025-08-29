import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        address TEXT
    )
""")
conn.commit()

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def format_gmail(username):
    username = username.strip().lower()
    if username == "":
        return ""
    if "@gmail.com" in username:
        return username
    return username + "@gmail.com"

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = format_gmail(email_entry.get())
    address = address_entry.get().strip()

    if name == "" or phone == "":
        messagebox.showerror("Error", "Name and Phone are required!")
        return

    if not is_valid_phone(phone):
        messagebox.showerror("Invalid Phone", "Phone number must be exactly 10 digits!")
        return

    if email and not email.endswith("@gmail.com"):
        messagebox.showerror("Invalid Email", "Email must end with @gmail.com")
        return

    cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                   (name, phone, email, address))
    conn.commit()
    clear_entries()
    fetch_contacts()
    messagebox.showinfo("Success", "Contact added successfully!")

def fetch_contacts():
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    contact_list.delete(*contact_list.get_children())
    for row in rows:
        contact_list.insert("", tk.END, values=row)

def search_contact():
    query = search_entry.get().strip()
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", ('%' + query + '%', '%' + query + '%'))
    rows = cursor.fetchall()
    contact_list.delete(*contact_list.get_children())
    for row in rows:
        contact_list.insert("", tk.END, values=row)

def delete_contact():
    selected = contact_list.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a contact to delete!")
        return

    values = contact_list.item(selected, "values")
    cursor.execute("DELETE FROM contacts WHERE id=?", (values[0],))
    conn.commit()
    fetch_contacts()
    messagebox.showinfo("Deleted", "Contact deleted successfully!")

def update_contact():
    selected = contact_list.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a contact to update!")
        return

    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = format_gmail(email_entry.get())
    address = address_entry.get().strip()
    values = contact_list.item(selected, "values")

    if not is_valid_phone(phone):
        messagebox.showerror("Invalid Phone", "Phone number must be exactly 10 digits!")
        return

    if email and not email.endswith("@gmail.com"):
        messagebox.showerror("Invalid Email", "Email must end with @gmail.com")
        return

    cursor.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                   (name, phone, email, address, values[0]))
    conn.commit()
    fetch_contacts()
    messagebox.showinfo("Updated", "Contact updated successfully!")

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def exit_app():
    cursor.close()
    conn.close()
    root.destroy()

root = tk.Tk()
root.title("📒 Contact Book")
root.attributes("-fullscreen", True)
root.config(bg="#101820")
root.resizable(False, False)

title_label = tk.Label(root, text="📒 Contact Book", font=("Helvetica", 40, "bold"), bg="#101820", fg="#00ffcc")
title_label.pack(pady=20)

frame = tk.Frame(root, bg="#101820")
frame.pack(pady=15)

tk.Label(frame, text="Name:", font=("Arial", 16, "bold"), bg="#101820", fg="white").grid(row=0, column=0, padx=15, pady=10)
name_entry = tk.Entry(frame, font=("Arial", 16), width=25, bg="#2c2c3c", fg="white")
name_entry.grid(row=0, column=1, padx=15, pady=10)

tk.Label(frame, text="Phone:", font=("Arial", 16, "bold"), bg="#101820", fg="white").grid(row=0, column=2, padx=15, pady=10)
phone_entry = tk.Entry(frame, font=("Arial", 16), width=25, bg="#2c2c3c", fg="white")
phone_entry.grid(row=0, column=3, padx=15, pady=10)

tk.Label(frame, text="Gmail Username:", font=("Arial", 16, "bold"), bg="#101820", fg="white").grid(row=1, column=0, padx=15, pady=10)
email_entry = tk.Entry(frame, font=("Arial", 16), width=25, bg="#2c2c3c", fg="white")
email_entry.grid(row=1, column=1, padx=15, pady=10)

tk.Label(frame, text="Address:", font=("Arial", 16, "bold"), bg="#101820", fg="white").grid(row=1, column=2, padx=15, pady=10)
address_entry = tk.Entry(frame, font=("Arial", 16), width=25, bg="#2c2c3c", fg="white")
address_entry.grid(row=1, column=3, padx=15, pady=10)

btn_frame = tk.Frame(root, bg="#101820")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="➕ Add", command=add_contact, width=15, height=2, font=("Arial", 14, "bold"),
          bg="#27ae60", fg="white").grid(row=0, column=0, padx=20)
tk.Button(btn_frame, text="🔄 Update", command=update_contact, width=15, height=2, font=("Arial", 14, "bold"),
          bg="#f39c12", fg="white").grid(row=0, column=1, padx=20)
tk.Button(btn_frame, text="❌ Delete", command=delete_contact, width=15, height=2, font=("Arial", 14, "bold"),
          bg="#e74c3c", fg="white").grid(row=0, column=2, padx=20)
tk.Button(btn_frame, text="🔍 Search", command=search_contact, width=15, height=2, font=("Arial", 14, "bold"),
          bg="#2980b9", fg="white").grid(row=0, column=3, padx=20)

search_entry = tk.Entry(btn_frame, font=("Arial", 14), width=20, bg="#2c2c3c", fg="white")
search_entry.grid(row=0, column=4, padx=15)

cols = ("ID", "Name", "Phone", "Email", "Address")
contact_list = ttk.Treeview(root, columns=cols, show="headings", height=15)

style = ttk.Style()
style.configure("Treeview", font=("Arial", 13), rowheight=30, background="#1c1c1c", foreground="white", fieldbackground="#1c1c1c")
style.configure("Treeview.Heading", font=("Arial", 15, "bold"), background="#00ffcc", foreground="black")

for col in cols:
    contact_list.heading(col, text=col)
    contact_list.column(col, width=250)

contact_list.pack(pady=20)
fetch_contacts()

bottom_frame = tk.Frame(root, bg="#101820")
bottom_frame.pack(pady=20)

tk.Button(bottom_frame, text="⏪ Clear Fields", command=clear_entries, width=20, height=2, font=("Arial", 14, "bold"),
          bg="#9b59b6", fg="white").grid(row=0, column=0, padx=30)
tk.Button(bottom_frame, text="❌ Exit", command=exit_app, width=20, height=2, font=("Arial", 14, "bold"),
          bg="#c0392b", fg="white").grid(row=0, column=1, padx=30)

root.mainloop()

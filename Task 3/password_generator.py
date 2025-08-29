import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            messagebox.showerror("Invalid Input", "Password length must be greater than 0.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copy_password():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Empty", "No password to copy!")

root = tk.Tk()
root.title("🔑 Password Generator")
root.geometry("400x300")
root.config(bg="#1e1e2f")

heading = tk.Label(root, text="🔐 Password Generator", font=("Helvetica", 18, "bold"), bg="#1e1e2f", fg="#00ffcc")
heading.pack(pady=15)

length_label = tk.Label(root, text="Enter Password Length:", font=("Arial", 12), bg="#1e1e2f", fg="white")
length_label.pack()
length_entry = tk.Entry(root, font=("Arial", 12), justify="center", width=15, bg="#2c2c3c", fg="white")
length_entry.pack(pady=5)

generate_btn = tk.Button(root, text="Generate Password", command=generate_password,
                         font=("Arial", 12, "bold"), bg="#00ffcc", fg="#1e1e2f", width=18)
generate_btn.pack(pady=10)

password_entry = tk.Entry(root, font=("Arial", 14), justify="center", width=30, bg="#2c2c3c", fg="#00ffcc")
password_entry.pack(pady=5)

copy_btn = tk.Button(root, text="Copy Password", command=copy_password,
                     font=("Arial", 12, "bold"), bg="#ff6f61", fg="white", width=15)
copy_btn.pack(pady=15)

root.mainloop()

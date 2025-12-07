import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

FILENAME = "students.csv"

# Ensure CSV exists
if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Email", "Grade"])

# Helper functions
def read_students():
    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_students(students):
    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Name", "Email", "Grade"])
        writer.writeheader()
        writer.writerows(students)

def next_id():
    students = read_students()
    return str(len(students))

# GUI Functions
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for student in read_students():
        tree.insert("", "end", values=(student["ID"], student["Name"], student["Email"], student["Grade"]))

def add_student():
    name = name_var.get().strip()
    email = email_var.get().strip()
    grade = grade_var.get().strip()
    if not name or not email or not grade:
        messagebox.showerror("Error", "All fields are required.")
        return
    sid = next_id()
    students = read_students()
    students.append({"ID": sid, "Name": name, "Email": email, "Grade": grade})
    write_students(students)
    messagebox.showinfo("Success", f"Student {name} added with ID {sid}")
    clear_fields()
    refresh_table()

def clear_fields():
    name_var.set("")
    email_var.set("")
    grade_var.set("")

def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a student to delete.")
        return
    values = tree.item(selected, "values")
    sid = values[0]
    students = [s for s in read_students() if s["ID"] != sid]
    write_students(students)
    messagebox.showinfo("Deleted", f"Student ID {sid} deleted.")
    refresh_table()

def edit_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a student to edit.")
        return
    values = tree.item(selected, "values")
    sid = values[0]

    students = read_students()
    for s in students:
        if s["ID"] == sid:
            s["Name"] = name_var.get() or s["Name"]
            s["Email"] = email_var.get() or s["Email"]
            s["Grade"] = grade_var.get() or s["Grade"]
            break
    write_students(students)
    messagebox.showinfo("Updated", f"Student ID {sid} updated.")
    clear_fields()
    refresh_table()

def on_select(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        name_var.set(values[1])
        email_var.set(values[2])
        grade_var.set(values[3])

# GUI setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x500")

# Input fields
name_var = tk.StringVar()
email_var = tk.StringVar()
grade_var = tk.StringVar()

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(frame, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(frame, textvariable=email_var).grid(row=1, column=1, padx=5, pady=5)
tk.Label(frame, text="Grade").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(frame, textvariable=grade_var).grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame, text="Add Student", command=add_student, bg="#4CAF50", fg="white").grid(row=3, column=0, pady=10)
tk.Button(frame, text="Edit Student", command=edit_student, bg="#FFC107", fg="white").grid(row=3, column=1, pady=10)
tk.Button(frame, text="Delete Student", command=delete_student, bg="#F44336", fg="white").grid(row=3, column=2, pady=10)

# Table
cols = ("ID", "Name", "Email", "Grade")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True, padx=20)
tree.bind("<<TreeviewSelect>>", on_select)

# Initial load
refresh_table()

root.mainloop()

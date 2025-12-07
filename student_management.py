import csv
import os

FILENAME = "students.csv"

# Ensure CSV file exists
if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Email", "Grade"])

# Function to generate next ID
def next_id():
    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        return str(len(rows))  # First row is header

# Add student
def add_student():
    name = input("Enter student name: ").strip()
    email = input("Enter student email: ").strip()
    grade = input("Enter student grade: ").strip()
    sid = next_id()
    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([sid, name, email, grade])
    print(f"✅ Student {name} added with ID {sid}.\n")

# View all students
def view_students():
    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print("\t".join(row))
    print()

# Search student by ID
def search_student():
    sid = input("Enter student ID to search: ").strip()
    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == sid:
                print(f"Found: ID={row['ID']}, Name={row['Name']}, Email={row['Email']}, Grade={row['Grade']}\n")
                return
    print("❌ Student not found.\n")

# Edit student by ID
def edit_student():
    sid = input("Enter student ID to edit: ").strip()
    students = []
    found = False
    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == sid:
                print(f"Editing {row['Name']}")
                row["Name"] = input(f"New name [{row['Name']}]: ") or row["Name"]
                row["Email"] = input(f"New email [{row['Email']}]: ") or row["Email"]
                row["Grade"] = input(f"New grade [{row['Grade']}]: ") or row["Grade"]
                found = True
            students.append(row)
    if not found:
        print("❌ Student not found.\n")
        return
    # Write back updated CSV
    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Name", "Email", "Grade"])
        writer.writeheader()
        writer.writerows(students)
    print("✅ Student updated.\n")

# Delete student by ID
def delete_student():
    sid = input("Enter student ID to delete: ").strip()
    students = []
    found = False
    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == sid:
                found = True
                continue
            students.append(row)
    if not found:
        print("❌ Student not found.\n")
        return
    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Name", "Email", "Grade"])
        writer.writeheader()
        writer.writerows(students)
    print("✅ Student deleted.\n")

# Main menu
def menu():
    while True:
        print("===== Student Management System =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Edit Student")
        print("5. Delete Student")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()
        print()
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            edit_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice, try again.\n")

if __name__ == "__main__":
    menu()

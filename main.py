import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Global variable to track the original rank during update
original_rank = None

def validate_form():
    fields = [
        ("First_Name", first_name_entry.get()),
        ("Last_Name", last_name_entry.get()),
        ("Gender", gender_combobox.get()),
        ("Age", age_spinbox.get()),
        ("Address", address_entry.get()),
        ("IOE_Rank", rank_entry.get()),
        ("Priority_1", numcourses1_combobox.get()),
        ("Priority_2", numcourses2_combobox.get()),
        ("Priority_3", numcourses3_combobox.get()),
        ("Guardian_Name", guardian_entry.get()),
        ("Contact", contact_entry.get()),
        ("Occupation", occupation_entry.get())
    ]

    for field_name, value in fields:
        if not value:
            messagebox.showerror("Error", f"{field_name} is required!")
            return

    data = {field_name: value for field_name, value in fields}
    rank = data["IOE_Rank"]

    # Check if rank already exists
    conn = sqlite3.connect('StudentData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Student_Data WHERE IOE_Rank = ?", (rank,))
    if cursor.fetchone():
        messagebox.showerror("Error", "IOE Rank must be unique!")
        conn.close()
        return
    conn.close()

    # Insert new record
    conn = sqlite3.connect('StudentData.db')
    insert_query = '''INSERT INTO Student_Data VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''
    cursor = conn.cursor()
    cursor.execute(insert_query, tuple(data.values()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Data saved successfully!")
    clear_form()

def clear_form():
    first_name_entry.delete(0, tkinter.END)
    last_name_entry.delete(0, tkinter.END)
    gender_combobox.set('')
    age_spinbox.delete(0, tkinter.END)
    age_spinbox.insert(0, "18")
    address_entry.delete(0, tkinter.END)
    rank_entry.delete(0, tkinter.END)
    numcourses1_combobox.set('')
    numcourses2_combobox.set('')
    numcourses3_combobox.set('')
    guardian_entry.delete(0, tkinter.END)
    contact_entry.delete(0, tkinter.END)
    occupation_entry.delete(0, tkinter.END)
    global original_rank
    original_rank = None

def search_student():
    search_rank = search_rank_entry.get()
    if not search_rank:
        messagebox.showerror("Error", "Enter IOE Rank to search!")
        return

    conn = sqlite3.connect('StudentData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student_Data WHERE IOE_Rank = ?", (search_rank,))
    result = cursor.fetchone()
    conn.close()

    if result:
        global original_rank
        original_rank = search_rank
        first_name_entry.delete(0, tkinter.END)
        first_name_entry.insert(0, result[0])
        last_name_entry.delete(0, tkinter.END)
        last_name_entry.insert(0, result[1])
        gender_combobox.set(result[2])
        age_spinbox.delete(0, tkinter.END)
        age_spinbox.insert(0, result[3])
        address_entry.delete(0, tkinter.END)
        address_entry.insert(0, result[4])
        rank_entry.delete(0, tkinter.END)
        rank_entry.insert(0, result[5])
        numcourses1_combobox.set(result[6])
        numcourses2_combobox.set(result[7])
        numcourses3_combobox.set(result[8])
        guardian_entry.delete(0, tkinter.END)
        guardian_entry.insert(0, result[9])
        contact_entry.delete(0, tkinter.END)
        contact_entry.insert(0, result[10])
        occupation_entry.delete(0, tkinter.END)
        occupation_entry.insert(0, result[11])
    else:
        messagebox.showinfo("Not Found", "No student found with this rank")

def delete_student():
    global original_rank
    if not original_rank:
        messagebox.showerror("Error", "Search for a student first!")
        return

    confirm = messagebox.askyesno("Confirm", "Delete this student's record?")
    if not confirm:
        return

    conn = sqlite3.connect('StudentData.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Student_Data WHERE IOE_Rank = ?", (original_rank,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Record deleted successfully!")
    clear_form()

def update_student():
    global original_rank
    if not original_rank:
        messagebox.showerror("Error", "Search for a student first!")
        return

    new_rank = rank_entry.get()
    if new_rank != original_rank:
        conn = sqlite3.connect('StudentData.db')
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Student_Data WHERE IOE_Rank = ?", (new_rank,))
        if cursor.fetchone():
            messagebox.showerror("Error", "IOE Rank already exists!")
            conn.close()
            return
        conn.close()

    update_data = (
        first_name_entry.get(),
        last_name_entry.get(),
        gender_combobox.get(),
        age_spinbox.get(),
        address_entry.get(),
        new_rank,
        numcourses1_combobox.get(),
        numcourses2_combobox.get(),
        numcourses3_combobox.get(),
        guardian_entry.get(),
        contact_entry.get(),
        occupation_entry.get(),
        original_rank
    )

    conn = sqlite3.connect('StudentData.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE Student_Data SET 
        First_Name=?, Last_Name=?, Gender=?, Age=?, Address=?, IOE_Rank=?, 
        Priority_1=?, Priority_2=?, Priority_3=?, Guardian_Name=?, Contact=?, Occupation=?
        WHERE IOE_Rank=?''', update_data)
    conn.commit()
    conn.close()
    original_rank = new_rank
    messagebox.showinfo("Success", "Record updated successfully!")

# Initialize database
conn = sqlite3.connect('StudentData.db')
conn.execute('''CREATE TABLE IF NOT EXISTS Student_Data
             (First_Name TEXT, Last_Name TEXT, Gender TEXT, Age INT, 
              Address TEXT, IOE_Rank INT PRIMARY KEY, Priority_1 TEXT, 
              Priority_2 TEXT, Priority_3 TEXT, Guardian_Name TEXT, 
              Contact INT, Occupation TEXT)''')
conn.close()

# GUI setup
window = tkinter.Tk()
window.title("Student Registration Form")

frame = tkinter.Frame(window)
frame.pack(padx=10, pady=10)

# Validation for numeric entries (for IOE_Rank and Contact)
validate_command = window.register(lambda new_value: new_value == "" or (new_value.isdigit() and len(new_value) <= 10))
validate_text_cmd = window.register(lambda new_value: new_value == "" or new_value.isalpha())



# User Information
user_info = tkinter.LabelFrame(frame, text="User Information")
user_info.grid(row=0, column=0, padx=10, pady=10)

tkinter.Label(user_info, text="First Name").grid(row=0, column=0)
tkinter.Label(user_info, text="Last Name").grid(row=0, column=1)
tkinter.Label(user_info, text="Gender").grid(row=0, column=2)

first_name_entry = tkinter.Entry(user_info, validate="key", validatecommand=(validate_text_cmd, "%P"))
last_name_entry = tkinter.Entry(user_info, validate="key", validatecommand=(validate_text_cmd, "%P"))
gender_combobox = ttk.Combobox(user_info, values=["Male", "Female", "Other"])

first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)
gender_combobox.grid(row=1, column=2)

tkinter.Label(user_info, text="Age").grid(row=2, column=0)
tkinter.Label(user_info, text="Address").grid(row=2, column=1)
tkinter.Label(user_info, text="IOE Rank" ).grid(row=2, column=2)

age_spinbox = tkinter.Spinbox(user_info, from_=18, to=100)
address_entry = tkinter.Entry(user_info, validate="key", validatecommand=(validate_text_cmd, "%P"))
rank_entry = tkinter.Entry(user_info, validate="key", validatecommand=(validate_command, "%P"))

age_spinbox.grid(row=3, column=0)
address_entry.grid(row=3, column=1)
rank_entry.grid(row=3, column=2)

for widget in user_info.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Courses Information
courses_frame = tkinter.LabelFrame(frame, text="Interested Faculty")
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

tkinter.Label(courses_frame, text="1st Priority").grid(row=0, column=0)
tkinter.Label(courses_frame, text="2nd Priority").grid(row=0, column=1)
tkinter.Label(courses_frame, text="3rd Priority").grid(row=0, column=2)

courses = ["Computer Engineering", "Civil Engineering", 
           "Electrical Engineering", "Electronics Engineering"]
numcourses1_combobox = ttk.Combobox(courses_frame, values=courses)
numcourses2_combobox = ttk.Combobox(courses_frame, values=courses)
numcourses3_combobox = ttk.Combobox(courses_frame, values=courses)

numcourses1_combobox.grid(row=1, column=0, padx=10, pady=5)
numcourses2_combobox.grid(row=1, column=1, padx=10, pady=5)
numcourses3_combobox.grid(row=1, column=2, padx=10, pady=5)

# Guardian Information
guardian_info = tkinter.LabelFrame(frame, text="Guardian Information")
guardian_info.grid(row=2, column=0, sticky="news", padx=20, pady=10)

tkinter.Label(guardian_info, text="Name").grid(row=0, column=0)
tkinter.Label(guardian_info, text="Contact").grid(row=0, column=1)
tkinter.Label(guardian_info, text="Occupation").grid(row=0, column=2)

guardian_entry = tkinter.Entry(guardian_info, validate="key", validatecommand=(validate_text_cmd, "%P"))
contact_entry = tkinter.Entry(guardian_info, validate="key", validatecommand=(validate_command, "%P"))
occupation_entry = tkinter.Entry(guardian_info, validate="key", validatecommand=(validate_text_cmd, "%P"))

guardian_entry.grid(row=1, column=0, padx=10, pady=5)
contact_entry.grid(row=1, column=1, padx=10, pady=5)
occupation_entry.grid(row=1, column=2, padx=10, pady=5)

# Search Section
search_frame = tkinter.LabelFrame(frame, text="Search/Edit Student")
search_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

tkinter.Label(search_frame, text="Enter IOE Rank:").grid(row=0, column=0)
search_rank_entry = tkinter.Entry(search_frame, validate="key", validatecommand=(validate_command, "%P"))
search_rank_entry.grid(row=0, column=1, padx=20, pady=10, sticky="news")
tkinter.Button(search_frame, text="Search", command=search_student).grid(row=0, column=2, padx=10, pady=5)
tkinter.Button(search_frame, text="Delete", command=delete_student).grid(row=0, column=3, padx=10, pady=5)
tkinter.Button(search_frame, text="Update", command=update_student).grid(row=0, column=4, padx=10, pady=5)

# Buttons
button_frame = tkinter.Frame(frame)
button_frame.grid(row=4, column=0, pady=10, padx=20, sticky="ew")
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
tkinter.Button(button_frame, text="Submit", command=validate_form).grid(row=0, column=0, padx=10, sticky="ew")
tkinter.Button(button_frame, text="Clear", command=clear_form).grid(row=0, column=1, padx=10, sticky="ew")

window.mainloop()
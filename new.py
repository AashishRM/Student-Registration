import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def validate_form():
    fields = [
        # User Information
        ("First_Name", first_name_entry.get()),
        ("Last_Name", last_name_entry.get()),
        ("Gender", gender_combobox.get()),
        ("Age", age_spinbox.get()),
        ("Address", address_entry.get()),
        ("IOE_Rank", rank_entry.get()),
        
        # Course Information
        ("Priority_1", numcourses1_combobox.get()),
        ("Priority_2", numcourses2_combobox.get()),
        ("Priority_3", numcourses3_combobox.get()),
        
        # Guardian Information
        ("Guardian_Name", guardian_entry.get()),
        ("Contact", contact_entry.get()),
        ("Occupation", occupation_entry.get())
    ]

    # It will Check if any field is empty
    for field_name, value in fields:
        if not value:
            messagebox.showerror("Error", f"{field_name} is required!")
            return

    messagebox.showinfo("Success", "Form submitted successfully!")
    print({field_name: value for field_name, value in fields})

    # It will Extract the values
    data = {field_name: value for field_name, value in fields}
    First_Name = data["First_Name"]
    Last_Name = data["Last_Name"]
    Gender = data["Gender"]
    Age = data["Age"]
    Address = data["Address"]
    IOE_Rank = data["IOE_Rank"]
    Priority_1 = data["Priority_1"]
    Priority_2 = data["Priority_2"]
    Priority_3 = data["Priority_3"]
    Guardian_Name = data["Guardian_Name"]
    Contact = data["Contact"]
    Occupation = data["Occupation"]

    conn = sqlite3.connect('StudentData.db')
    table_create_query = '''CREATE TABLE IF NOT EXISTS Student_Data
                            (First_Name TEXT, Last_Name TEXT, Gender TEXT, Age INT, Address TEXT, IOE_Rank INT,
                             Priority_1 TEXT, Priority_2 TEXT, Priority_3 TEXT, Guardian_Name TEXT, Contact INT, Occupation TEXT)
                         '''
    conn.execute(table_create_query)

    # It is to Insert data
    data_insert_query = '''INSERT INTO Student_Data 
                           (First_Name, Last_Name, Gender, Age, Address, IOE_Rank,
                            Priority_1, Priority_2, Priority_3, Guardian_Name, Contact, Occupation) 
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                        '''
    data_insert_tuple = (First_Name, Last_Name, Gender, Age, Address, IOE_Rank,
                         Priority_1, Priority_2, Priority_3, Guardian_Name, Contact, Occupation)

    cursor = conn.cursor()
    cursor.execute(data_insert_query, data_insert_tuple)
    conn.commit()
    conn.close()

def clear_form():
    """Clear all the input fields in the form."""
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

def search_student():
    """Search for a student by IOE Rank and fill the form with their information."""
    search_rank = search_rank_entry.get()
    if not search_rank:
        messagebox.showerror("Error", "IOE Rank is required for search!")
        return

    conn = sqlite3.connect('StudentData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Student_Data WHERE IOE_Rank = ?", (search_rank,))
    result = cursor.fetchone()
    conn.close()

    if result:
        # It will fill in the registration form with the student data
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
        messagebox.showinfo("Not Found", "No student found with that IOE Rank")

# Main window
window = tkinter.Tk()
window.title("Student Registration Form")

frame = tkinter.Frame(window)
frame.pack()

# Validation for numeric entries (for IOE_Rank and Contact)
validate_command = window.register(lambda new_value: new_value == "" or (new_value.isdigit() and len(new_value) <= 10))

# User Information Frame
user_info_frame = tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

first_name_label = tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

gender_label = tkinter.Label(user_info_frame, text="Gender")
gender_combobox = ttk.Combobox(user_info_frame, values=["Male", "Female", "Other"])
gender_label.grid(row=0, column=2)
gender_combobox.grid(row=1, column=2)

age_label = tkinter.Label(user_info_frame, text="Age")
age_spinbox = tkinter.Spinbox(user_info_frame, from_=18, to=110)
age_label.grid(row=2, column=0)
age_spinbox.grid(row=3, column=0)

address_label = tkinter.Label(user_info_frame, text="Address")
address_entry = tkinter.Entry(user_info_frame)
address_label.grid(row=2, column=1)
address_entry.grid(row=3, column=1)

rank_label = tkinter.Label(user_info_frame, text="IOE-Rank")
rank_entry = tkinter.Entry(user_info_frame, validate="key", validatecommand=(validate_command, "%P"))
rank_label.grid(row=2, column=2)
rank_entry.grid(row=3, column=2)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Courses Frame
courses_frame = tkinter.LabelFrame(frame, text="Interested Faculty")
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

numcourses1_label = tkinter.Label(courses_frame, text="1st Priority")
numcourses1_combobox = ttk.Combobox(courses_frame, values=["Computer Engineering", "Civil Engineering", "Electrical Engineering", "Electronics Engineering"])
numcourses1_label.grid(row=0, column=0)
numcourses1_combobox.grid(row=1, column=0)

numcourses2_label = tkinter.Label(courses_frame, text="2nd Priority")
numcourses2_combobox = ttk.Combobox(courses_frame, values=["Computer Engineering", "Civil Engineering", "Electrical Engineering", "Electronics Engineering"])
numcourses2_label.grid(row=0, column=1)
numcourses2_combobox.grid(row=1, column=1)

numcourses3_label = tkinter.Label(courses_frame, text="3rd Priority")
numcourses3_combobox = ttk.Combobox(courses_frame, values=["Computer Engineering", "Civil Engineering", "Electrical Engineering", "Electronics Engineering"])
numcourses3_label.grid(row=0, column=2)
numcourses3_combobox.grid(row=1, column=2)

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Guardian Information Frame
parents_frame = tkinter.LabelFrame(frame, text="Guardian Information")
parents_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

guardian_label = tkinter.Label(parents_frame, text="Name")
guardian_label.grid(row=0, column=0)
guardian_entry = tkinter.Entry(parents_frame)
guardian_entry.grid(row=1, column=0)

contact_label = tkinter.Label(parents_frame, text="Contact")
contact_entry = tkinter.Entry(parents_frame, validate="key", validatecommand=(validate_command, "%P"))
contact_label.grid(row=0, column=1)
contact_entry.grid(row=1, column=1)

occupation_label = tkinter.Label(parents_frame, text="Occupation")
occupation_label.grid(row=0, column=3)
occupation_entry = tkinter.Entry(parents_frame)
occupation_entry.grid(row=1, column=3)

for widget in parents_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Button Frame for Submit and Clear
button_frame = tkinter.Frame(frame)
button_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

# Configure two columns to have equal weight
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)

submit_button = tkinter.Button(button_frame, text="Enter Data", command=validate_form)
submit_button.grid(row=0, column=0, padx=10, sticky="ew")

clear_button = tkinter.Button(button_frame, text="Clear", command=clear_form)
clear_button.grid(row=0, column=1, padx=10, sticky="ew")

# Search Frame
search_frame = tkinter.LabelFrame(frame, text="Search Student")
search_frame.grid(row=4, column=0, sticky="news", padx=20, pady=10)

search_rank_label = tkinter.Label(search_frame, text="Enter IOE Rank:")
search_rank_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
search_rank_entry = tkinter.Entry(search_frame, validate="key", validatecommand=(validate_command, "%P"))
search_rank_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Configure the search frame so that all columns share space equally
search_frame.grid_columnconfigure(0, weight=1)
search_frame.grid_columnconfigure(1, weight=1)
search_frame.grid_columnconfigure(2, weight=1)

search_button = tkinter.Button(search_frame, text="Search", command=search_student)
search_button.grid(row=0, column=2, padx=10, pady=5)

window.mainloop()
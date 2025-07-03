📝 Student Registration Form (Tkinter + SQLite)
This is a Python GUI application built using Tkinter that allows users to:

- Fill in a student registration form
- Save data to a local SQLite database
- Search student data using IOE Rank
- Clear the form for new entries

📦 Features
✅ Collects user, guardian, and course priority information
✅ Validates form input (no empty fields)
✅ Saves data to an SQLite database (StudentData.db)
✅ Allows searching of a student by IOE Rank
✅ Clears all fields with one click

🖥️ GUI Sections

1. User Information
   First Name, Last Name
   Gender (dropdown)
   Age (spinbox)
   Address
   IOE Rank (number only)

2. Interested Faculty
   Priority 1, 2, 3 choices (dropdowns)

3. Guardian Information
   Guardian Name
   Contact (number only)
   Occupation

4. Search Student
   Search student by IOE Rank

📁 Database Table
The app creates a table named Student_Data with the following fields:

(First_Name, Last_Name, Gender, Age, Address, IOE_Rank, Priority_1, Priority_2, Priority_3, Guardian_Name, Contact, Occupation)

🛠️ Requirements
This project uses Python’s built-in libraries:

- tkinter for the GUI
- sqlite3 for the database
- ttk for styled widgets
- messagebox for popup messages
- No external libraries are required.

📌 Notes

- Fields like IOE Rank and Contact are restricted to digits only.
- You must fill out all fields before submitting.
- The database file (StudentData.db) is automatically created in the same folder.

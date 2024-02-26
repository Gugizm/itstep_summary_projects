import tkinter as tk
from tkinter import ttk, messagebox
from validation import InputValidation
from database import DataBase
from student import Student
import sqlite3


class StudentManagementApp:
    def __init__(self, root):
        self._validation = InputValidation()

        self._root = root
        self._root.title('Student Management System')
        self._root.geometry('800x400')

        self._menu_frame = ttk.Frame(root, padding=(10, 10), relief='solid')
        self._menu_frame.pack(side='left', fill='y')

        self._table_frame = ttk.Frame(root, padding=(10, 10), relief='solid')
        self._table_frame.pack(side='right', fill='both', expand=True)

        self.create_menu()
        self.create_table()

        self._database = DataBase(Student.class_name(), Student.sql_fields())
        self._empty_database = self._database.is_empty()
        self._load_data = self.show_all_students()


    def create_menu(self):
        self.clear_menu_frame()
        ttk.Label(self._menu_frame, text='Main Menu', font=("Helvetica", 14, "bold")).pack(pady=10)

        ttk.Button(self._menu_frame, text="Add a new student", width=20, command=self.show_add_student).pack(pady=5)
        ttk.Button(self._menu_frame, text="Get all students list", width=20, command=self.show_all_students).pack(pady=5)
        ttk.Button(self._menu_frame, text="Search students", width=20, command=self.search_by_frame).pack(pady=5)
        ttk.Button(self._menu_frame, text="Change student's info", width=20, command=self.show_change_info).pack(pady=5)
        ttk.Button(self._menu_frame, text="Delete student", width=20, command=self.show_delete_student).pack(pady=5)


    def create_table(self):
        # Create a treeview to display student data
        self.tree = ttk.Treeview(self._table_frame, columns=('Name', 'ID', 'Grade'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Grade', text='Grade')
        self.tree.pack(fill='both', expand=True)
        # self.tree.bind('<ButtonRelease-1>', self.on_tree_select)

    
    # def on_tree_select(self, event):
    # item = self.tree.selection()

    # if item:
    #     values = self.tree.item(item, 'values')

    #     ttk.Button(self._menu_frame, text="Change Information", width=20,
    #                command=lambda: self.show_change_info(values)).pack(pady=10)

    def show_add_student(self):
        self.clear_menu_frame()
        ttk.Label(self._menu_frame, text='Add Student', font=("Helvetica", 14, "bold")).pack(pady=10)

        ttk.Label(self._menu_frame, text='Name:').pack(pady=5)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(self._menu_frame, textvariable=name_var)
        name_entry.pack(pady=5)

        ttk.Label(self._menu_frame, text="Student's ID:").pack(pady=5)
        id_var = tk.StringVar()
        id_entry = ttk.Entry(self._menu_frame, textvariable=id_var)
        id_entry.pack(pady=5)

        ttk.Label(self._menu_frame, text='Grade:').pack(pady=5)
        grade_var = tk.StringVar()
        grades = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in range(0, len(grades), 3):
            row_frame = ttk.Frame(self._menu_frame)
            row_frame.pack()
            for j in range(3):
                index = i + j
                if index < len(grades):
                    ttk.Radiobutton(row_frame, text=grades[index], variable=grade_var, value=grades[index]).pack(side='left', padx=5)

        ttk.Button(self._menu_frame, text="Save Student", width=20,
                    command=lambda: self.save_student(name_var.get(), id_var.get(), grade_var.get())).pack(pady=10)

        ttk.Button(self._menu_frame, text="Back", width=20, command=self.create_menu).pack(pady=5)
        
        self.error_label = ttk.Label(self._menu_frame, text='', foreground='red')
        self.error_label.pack(pady=5)

    
    def save_student(self, name, id, grade):
        try:
            valid_id = self._validation.validate_id(id)
            valid_name = self._validation.validate_name(name)
            valid_grade = self._validation.validate_grade(grade)
        except ValueError as v:   
            self.error_label.config(text=v)
            return

        
        try:
            student = Student(valid_id, valid_name, valid_grade) 
            self._database.insert_data(student.dict())
            self.tree.insert('', 'end', values=(student.name, student.id, student.grade))
            self.show_add_student()
            messagebox.showinfo("Add student", "Student added successfully.")
        except sqlite3.Error:
            self.error_label.config(text=f'Student with {id} already exists!')



    def show_all_students(self):
        if not self._empty_database:
            self.clear_table_frame()
            fetched = self._database.get_all_data()
            students = self.unpack_student(fetched)
            self.display_students(students)



    def display_students(self, students):
        self.clear_table_frame()
        if isinstance(students, Student):
            self.tree.insert('', 'end', values=(students.id, students.name, students.grade))
        else:
            for student in students:
                self.tree.insert('', 'end', values=(student.id, student.name, student.grade))


    def search_by_frame(self):
        self.clear_menu_frame()

        ttk.Label(self._menu_frame, text='Search Students', font=("Helvetica", 12, "bold")).pack(pady=10)
        ttk.Label(self._menu_frame, text="Search Type:").pack(pady=5)
       
        search_type_var = tk.StringVar()
        search_type_var.set("ID  ")  
        for search_type in ["ID", "Name", "Grade"]:
            ttk.Radiobutton(self._menu_frame, text=search_type, variable=search_type_var, value=search_type).pack(padx=5) #need to add left or center id 

        ttk.Label(self._menu_frame, text="Search Value:").pack(pady=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(self._menu_frame, textvariable=search_var)
        search_entry.pack(pady=5)


        ttk.Button(self._menu_frame, text="Search", width=20,
                   command=lambda: self.display_search_results(search_type_var.get(), search_var.get())).pack(pady=10)

        ttk.Button(self._menu_frame, text="Back", width=20, command=self.create_menu).pack(pady=5)

        self.error_label = ttk.Label(self._menu_frame, text='', foreground='red')
        self.error_label.pack(pady=5)


    def display_search_results(self, search_type, value):
        if search_type == 'ID':
            try:
                valid = self._validation.validate_id(value)
                criteria = {'id': valid}
            except ValueError as v:   
                self.error_label.config(text=v)
        
        elif search_type == 'Name':
            try:
                valid = self._validation.validate_name(value)
                criteria = {'name': valid}
            except ValueError as v:   
                self.error_label.config(text=v)
        
        elif search_type == 'Grade':
            try:
                valid = self._validation.validate_grade(value)
                criteria = {'grade': valid}
            except ValueError as v:   
                self.error_label.config(text=v)
        
        fetched_data = self._database.get_by_criteria(criteria)
        try:
            students = self.unpack_student(fetched_data)
            print(students.name)
            self.display_students(students)
        except ValueError:
            key = list(criteria.keys())[0]
            self.error_label.config(text=f'Can not find student with {key} - {criteria[key]}')
     

    def show_change_info(self):
        self.clear_menu_frame()

        ttk.Label(self._menu_frame, text='Update Students', font=("Helvetica", 12, "bold")).pack(pady=10)
        ttk.Label(self._menu_frame, text="Update Type:").pack(pady=5)
       
        Update_type_var = tk.StringVar()
        Update_type_var.set("ID  ")  
        for Update_type in ["ID", "Name", "Grade"]:
            ttk.Radiobutton(self._menu_frame, text=Update_type, variable=Update_type_var, value=Update_type).pack(padx=5) #need to add left or center id 

        ttk.Label(self._menu_frame, text="Update Value:").pack(pady=5)
        Update_var = tk.StringVar()
        Update_entry = ttk.Entry(self._menu_frame, textvariable=Update_var)
        Update_entry.pack(pady=5)


        ttk.Button(self._menu_frame, text="Update", width=20,
                   command=lambda: self.display_Update_results(Update_type_var.get(), Update_var.get())).pack(pady=10)

        ttk.Button(self._menu_frame, text="Back", width=20, command=self.create_menu).pack(pady=5)

        self.error_label = ttk.Label(self._menu_frame, text='', foreground='red')
        self.error_label.pack(pady=5)


    def display_Update_results(self, Update_type, value):
        pass
    #should add in searc invisible button if want to change  then can be changed    

    def show_delete_student(self):
        pass

    def handel_empty_database(self):
        if self._database.is_empty():
            messagebox.showinfo("Student Database", "Try to add students")
            return True
        return False
    
    def unpack_student(self, data):
        if len(data) > 1:
            return [Student(student[0], student[1], student[2]) for student in data]
        return Student(data[0][0], data[0][1], data[0][2])

    def clear_menu_frame(self):
        for widget in self._menu_frame.winfo_children():
            widget.destroy()
    
    def clear_table_frame(self):
        for item in self.tree.get_children():
            self.tree.delete(item)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()

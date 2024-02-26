import sqlite3
from database import DataBase
from student import Student
from validation import InputValidation
from prettytable import PrettyTable
from display import Display

#taking data from database validation - while loop and try for non valid data to change valuse
class StudentManagmentSystem:
    def __init__(self, display): #need to add data_path
        self._database = DataBase(Student.class_name(), Student.sql_fields())
        self._validation = InputValidation()
        self._display = display
        self._empty_database = self._database.is_empty()
        
        
    
    def handel_empty_database(self):
        if self._empty_database:
            print('\nThe database of students is empty!')
            print('Please add a student first.')
            self.add_student()
            return True
        return False


    def unpack_student(self, data):
        if not data:
            raise ValueError("No data to unpack") #this should change 
        elif len(data) > 1:
            return [Student(student[0], student[1], student[2]) for student in data]
        return Student(data[0][0], data[0][1], data[0][2])


    def add_student(self):
        header = 'Add Student'
        row = 'Please enter student information'
        self._display.prompt(header, row)
        name = self._validation.validate_name()
        id = self._validation.validate_id()
        grade = self._validation.validate_grade()
        student = Student(id, name, grade) 
       
        try:
            self._database.insert_data(student.dict())
        except sqlite3.Error as e:
            self._display.table(student)
            header = 'Error'
            print(f'Student with {student.id} already exists!')

        if self._database.get_by_criteria(student.dict()):
            print('Student added successfully.')
            self._display.table(student)

            if self._empty_database:
                self._empty_database = False


        

    def get_all_students(self):
        if not self.handel_empty_database():
            fetched = self._database.get_all_data()
            student_list = self.unpack_student(fetched)
            self._display.table(student_list)


    def get_student_by_id(self):
        if not self.handel_empty_database():
            id = self._validation.validate_id() # he can be deleted new=false
            student = self.get_student_by({'id': id}, self.get_student_by_id)
            return student
    

    def get_students_by_name(self):
        if not self.handel_empty_database():
            name = self._validation.validate_name()
            self.get_student_by({'name': name}, self.get_students_by_name)


    def get_students_by_grade(self):
        if not self.handel_empty_database():
            grade = self._validation.validate_grade()
            # print(grade) #test
            self.get_student_by({'grade': grade}, self.get_students_by_grade)


    def get_student_by(self, criteria, func):
        fetched_data = self._database.get_by_criteria(criteria)
        try:
            students = self.unpack_student(fetched_data)
        except ValueError as v:
            key = list(criteria.keys())[0]
            print(f'Can not find student with {key} - {criteria[key]}')
            print('Try type again!')
            return func() 
        self._display.table(students)
        return students


    def prompt_update_grade(self):
        if not self.handel_empty_database():
            student = self.get_student_by_id()
            student.grade = self._validation.validate_grade()
            self.update_student(student, 'grade')


    def prompt_update_name(self):
        if not self.handel_empty_database():
            student = self.get_student_by_id()
            student.name = self._validation.validate_name()
            self.update_student(student, 'name')
  
  
    def update_student(self, student, text):
        self._database.update_by_criteria(student.dict())
        self._display.table(student)
        print(f"Student's {text} udated successfully.")


    def promt_delete_student(self):
        if not self.handel_empty_database():
            student = self.get_student_by_id()
            print('A deleted student will not be reinstated')
            choice = self._validation.yes_no()
            if choice == 'yes':
                self._database.delete_row(student.dict()) #delete object
                if not self._database.get_by_criteria(student.dict()):
                    del student
                    print('Student delated successfully.')
        
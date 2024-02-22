import re, os
import pyinputplus as pyip
import csv
from prettytable import PrettyTable, from_csv


class Student:
    def __init__(self, roll_number: int, name: str, grade: str):
        #validation of the received arguments
        assert isinstance(name, str), "Allowed only letters"
        assert isinstance(roll_number, int), "Allowed only numbers"
        assert isinstance(grade, str) and re.match('^[A-F]$', grade), "Alowed only upper letters from A to F"
        # Assign to self object
        self.__roll_number = roll_number
        self.__name = name
        self.__grade = grade

    
    def __str__(self):
        return f'{self.roll_number},{self.name},{self.grade}'

    @property
    def name(self):
        return self.__name
    
    @property
    def roll_number(self):
        return self.__roll_number
    
    @property
    def grade(self):
        return self.__grade
    
    @grade.setter
    def grade(self, new_grade):
        self.__grade = new_grade

    
class StudentManagementSystem:
    __csv_file = None
    __students = None
    __header = ['Roll Number', 'Name', 'Grade']
    
    def __init__(self):
        StudentManagementSystem.__csv_file = StudentManagementSystem.csv_path()
        StudentManagementSystem.__students = StudentManagementSystem.create_csv()


    @classmethod
    def csv_path(cls):
        folder_name = 'data'
        file_name = 'students.csv'
        current_path = os.getcwd()
        folder_path = os.path.join(current_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        return file_path


    @classmethod
    def create_csv(cls):
        try:
            with open(cls.__csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                return [Student(int(row[0]), row[1], row[2]) for row in reader]
        except FileNotFoundError:
            with open(cls.__csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(cls.__header)
                return []        


    @staticmethod
    def __display(students):
        if students:
            table = PrettyTable()
            table.field_names = StudentManagementSystem.__header
            if isinstance(students, Student):
                table.add_row([students.roll_number, students.name, students.grade])
            else:
                table.add_rows([student.roll_number, student.name, student.grade] for student in students)
            print(table.get_string())

            
    def add_new_student(self, roll_number, name, grade):
        student = Student(roll_number, name, grade)
        csv_list = [student.roll_number, student.name, student.grade]
        with open(StudentManagementSystem.__csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(csv_list)
                StudentManagementSystem.__students.append(student)
        self.__display(student)      
        print(f'{student.name} with {student.roll_number} roll number added successfully')


    

    def all_student(self):
        if not StudentManagementSystem.__students:
            raise ValueError('Student list is empty!\nPlease add student first.')
        self.__display(StudentManagementSystem.__students)
        

    def student_search(self, roll_number):
        if not StudentManagementSystem.__students:
            raise ValueError
        # self.__display(StudentManagementSystem.__students[0])3
        #need check if there is not a student id what to do
        for student in StudentManagementSystem.__students:
            if student.roll_number == roll_number:
                self.__display(student)
                return student
        else:
            raise TypeError
        

    def change_grade(self, student, grade):
        #student finde can be moved in main function
        student.grade = grade
        with open(StudentManagementSystem.__csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(StudentManagementSystem.__header)
            writer.writerows([student.roll_number, student.name, student.grade] for student in StudentManagementSystem.__students)
        print(f'{student.name} grade was successfully updated to {student.grade}')
        self.__display(student)




def add_student(sms, grades):
    print('Please enter student information:')
    name = input('Student name: ')
    roll_number = pyip.inputInt(prompt='Student roll number: ') #should be unic should change
    grade = pyip.inputMenu(grades, prompt='Enter grade of student:\n', lettered=True)
    sms.add_new_student(roll_number, name, grade)

def all_students(sms, grades):
    try:
        sms.all_student()
    except ValueError:
        print('Student list is empty!\nPlease add student first.')
        add_student(sms, grades)

def roll_student(sms, grades):
    while True:
        roll_number = pyip.inputInt(prompt='Please enter student roll number: ')
        try:
            student = sms.student_search(roll_number)
            break
        except TypeError:
            print(f'No student found with {roll_number} roll number')
            continue
        except ValueError:
            print('Student list is empty!\nPlease add student first.')
            add_student(sms, grades)
    return student

def change_grade(sms, grades):
    #this menu should be divided by functions and this choose will be call search_student and then other
    student = roll_student(sms, grades)
    grade = pyip.inputMenu(grades, prompt='Please enter one of the valid grade, below of menu\n', lettered=True)
    sms.change_grade(student, grade)

        
        
def main():
    sms = StudentManagementSystem()
    menu = ['Add a new student', 'Get all students list',
             'Get special student by roll number',
               "Change student's grade", 'EXIT\nEnter your option bellow  V']
    grades  = ['A', 'B', 'C', 'D', 'E', 'F']
    
    while True:
        choose = pyip.inputMenu(menu, prompt="Write a number of chosen option:\n", numbered=True)

        if choose == menu[0]:
            add_student(sms, grades)
            
        elif choose == menu[1]:
            all_students(sms, grades)

        elif choose == menu[2]:
            roll_student(sms, grades)

        elif choose == menu[3]:
            change_grade(sms, grades)
        
        elif choose == menu[4]:
            break


        cont = pyip.inputYesNo(prompt="Do you want to continue program YES/NO: ").lower()
        if cont == 'no':
            break

if __name__ == '__main__':
    main()

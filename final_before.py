import sys, os, sqlite3
from database import StudentsDataBase
from prettytable import PrettyTable


class Student:
    def __init__(self, roll_number: int, name: str, grade: str):
        self._validate = UserInputValidation()
        self._roll_number = self._validate.roll_number(roll_number)
        self._name = self._validate.name(name)
        self.grade = self._validate.grade(grade)


    @classmethod
    def students(cls):
        return cls._students


    @property
    def roll_number(self):
        return self._roll_number
    
    
    @property
    def name(self):
        return self._name
    
    
    @property
    def grade(self):
        return self._grade
    

    @grade.setter
    def grade(self, new_grade):
        self._grade = self._validate.grade(new_grade)



class EmptyListError(Exception):
    def __init__(self, message="No students found. Please add students firs."):
        self.message = message
        super().__init__(self.message)


class StudentsDataBase:
    def __init__(self, db_path=':memory:'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()


    def create_table(self):
        with self.conn:
            self.conn.execute("""CREATE TABLE IF NOT EXISTS students (
                              name TEXT,
                              roll_number INTEGER,
                              grade TEXT
                              )""")
    

    def save_new_student(self, student):
        with self.conn:
            self.conn.execute('INSERT INTO students VALUES (:name, :roll_number, :grade)', 
                            {'name': student.name, 'roll_number': student.roll_number, 'grade': student.grade})
            #here should add valdiation of rows think up after
    
            
    def get_all_students(self):
        with self.conn:
            # return self.conn.execute('SELECT * FROM students').fetchall()
            cursor = self.conn.execute('SELECT * FROM students')
            students = cursor.fetchall()
            if not students:
                raise ValueError('No students found. Please add students firs.')
            try:
                return [Student(student[0], student[1], student[2]) for student in students]
            except Exception as e:
                print(e) # maybe we do not need that
                print('The database file has been modified, the data does not match the student attribute validation!')
                

    def get_student_by_roll_number(self, roll_number):
        with self.conn:
            # return self.conn.execute('SELECT * FROM students WHERE roll_number = :roll_number',
            #                   {'roll_number': roll_number}).fetchone()
            cursor = self.conn.execute('SELECT * FROM students WHERE roll_number = :roll_number',
                              {'roll_number': roll_number})
            student = cursor.fetchone()
            if student is None:
                raise ValueError(f'No student found with {roll_number} roll number')
            return Student(student[0], student[1], student[2])
            # can return none maby return list and inside main file create student class
        
    
    def get_students_roll_numbers(self):
        with self.conn:
            cursor = self.conn.execute('SELECT roll_number FROM students')
            roll_numbers = cursor.fetchall()
            return [roll_number[0] for roll_number in roll_numbers]

    
    def update_grade(self, student):
        with self.conn:
            self.conn.execute('UPDATE students SET grade = :grade WHERE roll_number = :roll_number',
                              {'roll_number': student.roll_number, 'grade': student.grade})          


    def student_count(self):
        with self.conn:
            cursor = self.conn.execute('SELECT COUNT(*) FROM students')
            number_of_students = cursor.rowcount
            return number_of_students


class StudentManagementSystem:
    def __init__(self):
        self.data = StudentsDataBase()
        self.students = self.get_all_students() # do not need maybe
    

    def get_all_students(self):
        return self.self.data.get_all_students()
    

    # @staticmethod
    # def student_object_generator(students):
    #     if isinstance(students[0], str):
    #         return Student[students[0], students[1], students[2]]
        
    #     elif isinstance(students[0], tuple):
    #         return [Student[student[0], student[1], student[2]] for student in students]
        
    
    def add_student(self, name, roll_number, grade):
        self.data.add_student(Student(name, roll_number, grade))
        # print('Student added successfully')
        # need exception maybe


    def search_student(self, roll_number): #maybe vhange name
        try:
            return self.data.get_student_by_roll_number(roll_number)
        except IndexError:
            raise 
            
        roll_number = self._prompts.roll_number(self._roll_numbers)
        for student in self._students:
            if student.roll_number == roll_number:
                self.display(student)
                return student

        
    @classmethod
    def change_grade(cls):
        student = cls.search_student()
        student.grade = cls._prompts.grade()
        cls.save_students()
        cls.display(student)
        print(f'Grade was successfully updated to')


    @classmethod
    def display(cls, students):
        if students:
            table = PrettyTable()
            table.field_names = cls._csv_header
            if isinstance(students, Student):
                table.add_row([students.roll_number, students.name, students.grade])
            else:
                table.add_rows([student.roll_number, student.name, student.grade] for student in students)
            print('\n')
            print(table.get_string())



class UserInputValidation:
    # @classmethod
    # def initialization(cls):
    #     cls._sms = StudentManagementSystem()
    #     cls._options = ['Add a new student', 'Get all students list',
    #          'Get special student by roll number',
    #            "Change student's grade", 'EXIT']
    #     cls._grades = ['A', 'B', 'C', 'D', 'E', 'F']

    


        #ask in UserInputValidation continue or write agane with that roll_number
        


    # @classmethod
    # def roll_student(cls):
    #     roll_number = cls.validate_input('roll number: ', lambda x: Student.roll_number_validation(x))
    #     return roll_number
    @classmethod #should give list of roll numbers atribut
    def valid_roll_number(cls, new=True):
        if not new:
            roll_number = input('Roll numebr: ')

        try:
            roll_number = int(roll_number)
            if roll_number in roll_numbers():
                if create == True:
                    print(f'{roll_number} roll number already exists.')
                    return cls.roll_number(roll_numbers, create=True)
                return roll_number
            
            if create == True:
                return roll_number
            print(f'No student found with {roll_number} roll number')
            return cls.roll_number(create=True) #here maybe in UserInputValidation ask if user wants contunue
        
        except Exception:
            print('Roll number should be an integer!')
            return cls.roll_number(roll_numbers, create)


    @classmethod
    def valid_name(cls, new=True):
        while True:
            if new:
                name = input('Name: ')
            words = name.split()
            cleaned_name = " ".join([c_name.strip() for c_name in words])
            cleaned_name = name.strip()
            condition_1 = all(char.isalpha() or char.isspace() for char in cleaned_name)
            condition_2 = 1 <= len(cleaned_name) <= 40
            if condition_1 and condition_2:
                print('Not valid name!')
                print('Name should only contain letters and should be 1-40 characters.')
                continue
            
            return cleaned_name

    @classmethod
    def validate_input(prompt, validation_func):
        while True:    
            try:
                choice = input(prompt)
                return validation_func(choice)
            except ValueError as v:
                print(v)

    @classmethod
    def valid_grade(cls, grade):
            grades = ['A', 'B', 'C', 'D', 'E', 'F']
            print('Please enter one of the grades.')
            print('-'.join(grades))
            if grade.upper() in grades:
                return grade.upper()
            print('Invalide grade!')

    @classmethod
    def new_student(cls):
        print('To add a new student, please enter the following information.')
        name = cls.valid_input('Name: ', cls.valid_name)
        roll_number = cls.validate_input('Grade: ', cls.valid_roll_number)
        grade = cls.validate_input('Grade: ', cls.valid_grade)
        student = Student(name, roll_number, grade)
        StudentsDataBase.save_new_student(student)
        cls.display(student)
        print('Student added successfully')

    @classmethod
    def update_grade(cls):
        print('Please')
    # @classmethod
    # def prompt_student_info(cls):
    #     print('Please enter student information:')
    #     name = cls.validate_input('name: ', lambda x: Student.name_validation(x))
    #     roll_number = cls.validate_input('roll number: ', lambda x: Student.roll_number_validation(x, new_student=True))
    #     grade = cls.prompt_grade()
        
    #     student = cls._sms.add_student(roll_number, name, grade)

        #dispaly

    # @classmethod
    # def prompt_grade(cls):
    #     print('Please enter one of the grades:')
    #     print('-'.join(cls._grades))
    #     grade = cls.validate_input('Grade: ', lambda x: Student.grade_validation(x))
    #     return grade




    # @classmethod
    # def all_students(cls):
    #     try:
    #         cls._sms.all_student() # maybe need something
    #     except ValueError as v:
    #         print(v)


        

    # @classmethod
    # def change_grade(cls):
    #     roll_number = cls.roll_student()
    #     grade = cls.prompt_grade()
    #     return roll_number, grade        


def recru(data, func, text):
    while True:
        if not data.get_all_students(): #what i need
            print('The list of students is empty!')
            print('Please add a student first.')
            return data.add_student()
        func()

        while True:
            print(f'\n1. {text}')
            print('2. Main Menu')
            print('3. Exit')
            
            choice = input("\nWrite a number of chosen option: ")
            try:
                choice = int(choice)
                if 1 <= choice <= 5:
                    pass
            except Exception:
                print("Invalid choice. Please enter a valid option")
                continue
        
            if choice == 1:
                return recru(func, text)
            elif choice == 2:
                return main()
            elif choice == 3:
                break
        
        


    

        
def main():
    #before start program can be a info text that it makes a folder or can be writen help
    data = StudentsDataBase()
    options = ['Add a new student.', 'Get all students list.',
             'Get special student by roll number.',
               "Change student's grade.", 'EXIT.']
    
    while True:
        print('\nMain Menu')
        for num, option in enumerate(options, start=1):
            print(num, option)
        

        choice = input("\nWrite a number of chosen option: ")
        try:
            choice = int(choice)
            choice >= 1
            choice <= 5
        except Exception:
            print("Invalid choice. Please enter a valid option")
            continue

        if choice == 1:
            recru(data, data.add_student, options[choice - 1])
            
        elif choice == 2:
            data.get_all_students()

        elif choice == 3:
            recru(data, data.get_student_by_roll_number, options[choice - 1])

        elif choice == 4:
            recru(data, data.update_grade, options[choice - 1])
        
        elif choice == 5:
            break


if __name__ == '__main__':
    main()



#### so we should take validations in student class and merge system and UserInputValidation
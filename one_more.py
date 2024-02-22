import sys
from database import DataBase
from student import Student
from validation import InputValidation
from prettytable import from_db_cursor


class StudentManagmentSystem:
    def __init__(self): #need to add data_path
        self._database = DataBase(Student.class_name(), Student.sql_fields())
        self._existing_id = self._database.get_field_by_criterias('id').fetchall()
        self._validation = InputValidation(self._existing_id)
        self._students = [Student(*row) for row in self._database.get_all_data().fetchall()]


    @property
    def students(self):
        return [Student(*row) for row in self.database.get_all_data().fetchall()]
    

    @property
    def existing_id(self):
        return self._database.get_field_by_criterias('id').fetchall()

    @property
    def validation(self):
        return InputValidation(self.existing_id)
    
    @property
    def database(self):
        return self._database
    


    def add_student(self):
        print('\nPlease enter student information:')
        name = self._validation.validate_name()# can take name roll and grade outside and use here  can be capitalize
        id = self._validation.validate_id(new=True)
        grade = self._validation.validate_grade(new=True)
        student = Student(id, name, grade)
        self.database.insert_data(student.dict())
        cursor = self.database.get_by_criteria(student.dict())
        self.display_students(cursor)
        print('Student added successfully.')


    def get_all_students(self):
        cursor = self.database.get_all_data()
        rows = cursor.fetchall()
        if rows:
            self.display_students(cursor)
        else:
            print('\nThe database of students is empty!')
            print('Please add a student first.')
            self.add_student()


    def get_student_by_id(self):
        id = self._validation.validate_id(new=True)
        self.get_student_by({'id': id})
        return id
    

    def get_students_by_name(self):
        name = self._validation.validate_name()
        self.get_student_by({'name': name})


    def get_students_by_grade(self):
        grade = self._validation.validate_grade()
        self.get_student_by({'grade': grade})


    @classmethod
    def get_student_by(self, criteria):
        cursor = self.database.get_by_criteria(criteria)
        self.display_students(cursor)


    def prompt_update_grade(self):
        id = self.get_student_by_id()
        grade = self._validation.validate_grade(new=True)
        self.update_student('grade', grade, id)
        # for student in self.students:
        #     if student.id == id:
        #         student.grade = grade
        #         self.database.update_by_criteria(student.dict())
        #         cursor = self.database.get_by_criteria(student.dict())
        #         self.display_students(cursor)
        #         break
        print('Student grade updated successfully.')
    

    def prompt_update_name(self):
        id = self.get_student_by_id()
        name = self._validation.validate_name()
        self.update_student('name', name, id)
        # id = self.get_student_by_id()
        # name = self._validation.validate_name()
        # for student in self.students:
        #     if student.id == id:
        #         student.name = name
        #         self.database.update_by_criteria(student.dict())
        #         cursor = self.database.get_by_criteria(student.dict())
        #         self.display_students(cursor)
        #         break
        print('Student name updated successfully.')

    @classmethod
    def update_student(self, attribute, new_value, id):
        update_student_funcs = {
            'grade': student.grade,
            'name': student.name
        }
        for student in self.students:
            if student.id == id:
                update_student_funcs[attribute] = new_value
                self.database.update_by_criteria(student.dict())
                cursor = self.database.get_by_criteria(student.dict())
                self.display_students(cursor)
                break



    def promt_delete_student(self):
        id = self.get_student_by_id()
        print('A deleted student will not be reinstated')
        choice = self._validation.yes_no()
        if choice == 'yes':
            for student in self.students:
                if student.id == id:
                    self.database.delete_row(student.dict()) #delete object
                    del student
                    break
            print('Student deleted successfully.')
        else:
            return

    @classmethod
    def display_students(self, cursor):
        table = from_db_cursor(cursor)
        print(table.get_string())
    # def update_by_menu(self):
    #     header = ['Menu']
    #     options = ["Update student's grade", "Update student's name", 
    #                 'Main Menu', 'EXIT']
    #     prompt = "\nWrite a number of chosen option: "
    #     choice = self._validation.menu(header, options, prompt, self.display_menu)

    #     if choice == 1:
    #         return self.recru(self.prompt_update_grade, options[choice - 1])

    #     elif choice == 2:
    #         return self.recru(self.prompt_update_name, options[choice - 1])
        
    #     elif choice == 3:
    #         return self.main()

    #     elif choice == 4:
    #         sys.exit()

    

    # def get_student_by_menu(self):
    #     header = ['Menu']
    #     options = ['Get student by roll numbe', 'Get students by name', 
    #                'Get students by grade', 'Main Menu', 'EXIT']
    #     prompt = "\nWrite a number of chosen option: "
    #     choice = self._validation.menu(header, options, prompt, self.display_menu)

    #     if choice == 1:
    #         return self.recru(self.get_student_by_id, options[choice - 1])

    #     elif choice == 2:
    #         return self.recru(self.get_students_by_name, options[choice - 1])
        
    #     elif choice == 3:
    #         return self.recru(self.get_students_by_grade, options[choice - 1])
        
    #     elif choice == 4:
    #         return self.main()

    #     elif choice == 5:
    #         sys.exit()


    # def main(self):
    #     header = ['Main Menu']
    #     options = ['Add a new student.', 'Get all students list.',
    #         'Search students.',
    #         "Change student's grade.", 'EXIT.']
    #     prompt = "\nWrite a number of chosen option: "
    #     choice = self._validation.menu(header, options, prompt, self.display_menu)
       
    #     if choice == 1:
    #         return self.recru(self.add_student, options[choice - 1])
            
    #     elif choice == 2:
    #         self.recru(self.get_all_students, options[choice - 1]) #need to change

    #     elif choice == 3:
    #         return self.recru(self.get_student_by_menu, options[choice - 1])

    #     elif choice == 4:
    #         return self.recru(self.update_by_menu, options[choice - 1])
        
    #     elif choice == 5:
    #         sys.exit()

    # def recru(self, func, text):
    #     while True:
    #         if not self.students: #what i need
                # print('\nThe database of students is empty!') # can call display
                # print('Please add a student first.')
    #             return self.add_student() # add stuent should be inside
            
    #         func()

    #         header = ['Menu']
    #         options = [text, 'Main Menu', 'Exit']
    #         prompt = 'Write a number of chosen option: '
    #         choice = self._validation(header, options, prompt, self.display_menu)
                
    #         if choice == 1:
    #             return self.recru(func, text)
    #         elif choice == 2:
    #             return self.main()
    #         elif choice == 3:
    #             break #maby sys.exit


    # @classmethod
    # def display_menu(cls, header, options): #header can be =True
    #     table = PrettyTable()
    #     table.align = 'l'
    #     table.field_names = header
    #     for num, option in enumerate(options, start=1): #add enumarate
    #         table.add_row([f'{num}. {option}'])
    #     print(table.get_string())





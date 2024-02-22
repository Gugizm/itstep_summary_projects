import sys
from database import DataBase
from student import Student
from validation import InputValidation
from prettytable import from_db_cursor
from prettytable import PrettyTable

#taking data from database validation - while loop and try for non valid data to change valuse
class StudentManagmentSystem:
    def __init__(self): #need to add data_path
        self._database = DataBase(Student.class_name(), Student.sql_fields())
        self._validation = InputValidation()
        self._students = self.students()

    def students(self):
        data = self._database.get_all_data().fetchall()
        print([Student(*self._validation.validate_data_from_database(*row)).dict() for row in data])#test
        return [Student(*self._validation.validate_data_from_database(*row)) for row in data]
        #if updated after loaded data from database upload new data
       
    

    # @property
    # def existing_id(self):
    #     return self._database.get_field_by_criterias('id').fetchall()

    # @property
    # def validation(self):
    #     return InputValidation(self.existing_id)
      
    def existing_ids(self):
        result = self._database.get_field_by_criterias('id').fetchall()
        return [row[0] for row in result]
    

    def add_student(self):
        table = PrettyTable()
        row = table.add_row(['Please enter student information:'])
        # print('\nPlease enter student information:')
        print(table.get_string())
        name = self._validation.validate_name()# can take name roll and grade outside and use here  can be capitalize
        id = self._validation.validate_id()
        grade = self._validation.validate_grade()
        student = Student(id, name, grade)
        self.students.append(student)
        self._database.insert_data(student.dict())
        cursor = self._database.get_by_criteria(student.dict())
        self.display_students(cursor)
        print('Student added successfully.')


    def get_all_students(self):
        cursor = self._database.get_all_data()
        if self._students:
            self.display_students(cursor)
        else:
            print('\nThe database of students is empty!')
            print('Please add a student first.')
            self.add_student()


    def get_student_by_id(self):
        id = self._validation.validate_id(new=False)
        self.get_student_by({'id': id})
        return id
    

    def get_students_by_name(self):
        name = self._validation.validate_name()
        self.get_student_by({'name': name})


    def get_students_by_grade(self):
        grade = self._validation.validate_grade()
        # print(grade) #test
        self.get_student_by({'grade': grade})


    def get_student_by(self, criteria):
        cursor = self._database.get_by_criteria(criteria)
        # print(cursor.fetchall()) # test
        self.display_students(cursor)


    def prompt_update_grade(self):
        id = self.get_student_by_id()
        grade = self._validation.validate_grade()
        self.update_student('grade', grade, id)
        # for student in self.students:
        #     if student.id == id:
        #         student.grade = grade
        #         self._database.update_by_criteria(student.dict())
        #         cursor = self._database.get_by_criteria(student.dict())
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
        #         self._database.update_by_criteria(student.dict())
        #         cursor = self._database.get_by_criteria(student.dict())
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
                self._database.update_by_criteria(student.dict())
                cursor = self._database.get_by_criteria(student.dict())
                self.display_students(cursor)
                break



    def promt_delete_student(self):
        id = self.get_student_by_id()
        print('A deleted student will not be reinstated')
        choice = self._validation.yes_no()
        if choice == 'yes':
            for student in self.students:
                if student.id == id:
                    self._database.delete_row(student.dict()) #delete object
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





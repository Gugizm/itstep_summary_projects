from menu import StudentManagmentSystem
from validation import InputValidation
from new_menu import Menu

#add sleep
def main():
    run = StudentManagmentSystem()

    update_options = [
        "Update student's grade",
        "Update student's name"
        ]

    search_options = [
        'Get students by ID',
        'Get students by name',
        'Get students by grade'
        ]

    main_options = [
        'Add a new student.', 
        'Get all students list.',
        'Search students.',
        "Change student's info.",
        'Delete student'
        ]
    
    update_funcs = [
        run.prompt_update_grade,
        run.prompt_update_name
        ]
    
    search_funcs = [
        run.get_student_by_id,
        run.get_students_by_name,
        run.get_students_by_grade
        ]
    
    search_zip = list(zip(search_options, search_funcs))
    update_zip = list(zip(update_options, update_funcs))

    main_funcs = [
        run.add_student,
        run.get_all_students,
        search_zip,
        update_zip,
        run.promt_delete_student
        ]
    
    main_zip = list(zip(main_options, main_funcs))

    menu = Menu(main_zip, ['Student Management System'])
    menu.menu()

if __name__ == '__main__':
    main()

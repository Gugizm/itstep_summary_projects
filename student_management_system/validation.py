class InputValidation:


    def validate_name(self, new=False):
        while True:
            name = input('Name: ')
            if name.replace(' ', '').isalpha():
                cleaned_name = " ".join([c_name.strip().capitalize() for c_name in name.split()])
                return cleaned_name
            print('Name should only contain letters and spaces and should be 1-40 characters.')
            print('Try type again')
        

    def validate_id(self): #add to find to be new false
        while True:
            id = input("Student's ID: ")
            try:
                id = int(id)
                if id <= 0:
                    raise ValueError(f'ID should be a positive integer not {id}!')
                return id
            except ValueError as v:
                print(v)
                print('Please enter student ID.')
        
    
    def validate_grade(self): #should change in find
        grades = ['A', 'B', 'C', 'D', 'E', 'F']
        while True:
            print('Please enter one of the grades.') #maybe take in system or everything take here
            print('-'.join(grades))
            grade = input('Grade: ')
            if grade.upper() in grades:
                return grade.upper()
            
            print(f"'{grade}' is not valide input!") # errors can put inside table
                    # print(f"'{grade}' is not valide input!")

    
    def yes_no(self):
        options = ['yes', 'no']
        while True:
            choice = input('Confirm your choice (yes/no): ')
            if choice.lower() in options:
                return choice.lower()
            print('Please enter either "YES" or "NO".')
    
    
   
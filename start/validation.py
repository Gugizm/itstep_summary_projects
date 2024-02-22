class InputValidation:
    def __init__(self):
        self.ids = []
        self.grades = []
        print(self.grades) #test


    
    def validate_input(self, prompt, validation_func, *args, **kwargs):
        while True:    
            try:
                #need to add if from database validation
                choice = input(prompt)
                return validation_func(choice, *args, **kwargs)
            except Exception as v:
                print(v)
            continue


     #marge to upper validations 
    def validate_database(self, attar, func):
        try:
            print(attar)
            func(attar)
        except ValueError as v:
            print(f"""'{attar}' is not valide!\n
                    DataBase has changed manualy\n
                    {v}""")
            print("Let's make it valid")
            func()


    
    def validate_name(self, name=False):
        if not name:
            return self.validate_input('Name: ', self.validate_name)
        if isinstance(name, str):
            split_name = name.split()
            cleaned_name = name.strip()
            cleaned_name = " ".join([c_name.strip() for c_name in split_name])
            condition_1 = all(char.isalpha() or char.isspace() for char in cleaned_name)
            condition_2 = 1 <= len(cleaned_name) <= 40
            if condition_1 and condition_2:
                return cleaned_name
            raise Exception('Name should only contain letters and spaces and should be 1-40 characters.')


    def validate_id(self, id=False, new=True): #add to find to be new false
        
        if not id:
            print('Please enter student ID.')
            # id = input("Student's ID: ")
            if new:
                return self.validate_input('ID: ', self.validate_id, new=True)
            return self.validate_input('ID: ', self.validate_id)
     
        try:
            id = int(id)
        except ValueError:
            raise ValueError(f'ID should be an integer not {id}!')

        if id in self.ids:
            if new:

                raise ValueError(f'{id} ID already exists.\nID should be unic')
            return int(id) #do not need int firs will run then check
        
        elif new:
            self.ids.append(id)
            return id
        raise ValueError(f'No student found with {id} ID')
    

    
    def validate_grade(self, grade=None): #should change in find
        if grade is None:
            grades = ['A', 'B', 'C', 'D', 'E', 'F']
            print('Please enter one of the grades.')
            print('-'.join(grades))
            grade = self.validate_input('Grade: ', self.validate_grade)

            try:
                if isinstance(grade, str) and grade.upper() in grades:
                #if graid does not exists check
                    return grade.upper()
            except ValueError:
                non_valid = grade
                grade = None
                raise ValueError(f"'{non_valid}' is not valide input!")
                    # print(f"'{grade}' is not valide input!")

    
    def yes_no(self, choice=False):
        options = ['yes', 'no']
        if not choice:
            return self.validate_input('Confirm your choice (yes/no): ', self.yes_no)
        if choice.lower() in options:
            return choice.lower()
        raise ValueError('Please enter either "yes" or "no".')
    
        

    def validate_data_from_database(self, id, name, grade):
        print(id, name, grade) #test
        id = self.validate_database(id, self.validate_id)
        name = self.validate_database(name, self.validate_name)
        grade = self.validate_database(grade, self.validate_grade)
        return id, name, grade
        # try:
        #     self.validate_id(id)
        # except ValueError as v:
        #     print(f"""'{id}' is not valide!\n
        #             DataBase has changed manualy\n
        #             {v}""")
        #     print("Let's make id valid")
        #     self.validate_id()
        # try:
        #     self.validate_name(name)
        # except ValueError as v:
        #     print(f"""'{id}' is not valide!\n
        #             DataBase has changed manualy\n
        #             {v}""")
        #     print("Let's make id valid")
        #     self.validate_id()
        
        
        



class InputValidation:
    @staticmethod
    def validate_name(name):
        if name.replace(' ', '').isalpha() and len(name) <= 40:
            cleaned_name = " ".join([c_name.strip().capitalize() for c_name in name.split()])
            return cleaned_name
        raise ValueError('Name should only contain\nletters and spaces\nand should be 1-40 characters.')
        
    @staticmethod
    def validate_id(id):
        try:
            id = int(id)
            if id > 0:
                return id
        except ValueError:
            raise ValueError('ID should be positive integer!')
            
    @staticmethod
    def validate_grade(grade): #should change in find
        grades = ['A', 'B', 'C', 'D', 'E', 'F']
        if grade.upper() in grades:
            return grade.upper()
        raise ValueError('Please select grade')        

    @staticmethod
    def yes_no():
        options = ['yes', 'no']
        while True:
            choice = input('Confirm your choice (yes/no): ')
            if choice.lower() in options:
                return choice.lower()
            print('Please enter either "YES" or "NO".')
    

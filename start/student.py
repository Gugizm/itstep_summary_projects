from validation import InputValidation

class Student:
    def __init__(self, id, name, grade):
        self._id = id
        self.name = name
        self.grade = grade

#add delete student
    @property
    def id(self):
        return self._id
    
    
    @property
    def name(self):
        return self._name
    
    
    @property
    def grade(self):
        return self._grade
    
    @name.setter
    def name(self, new_name):
        self._name = new_name
    

    @grade.setter
    def grade(self, new_grade):
        self._grade = new_grade

    #could use __dict__ but then _ was problem
    def dict(self):
        return {'id': self._id, 'name': self._name, 'grade': self._grade}


    @classmethod
    def class_name(cls):
        return cls.__name__


    @classmethod
    def sql_fields(cls):
        return 'id INTEGER, name TEXT, grade TEXT'
    
    



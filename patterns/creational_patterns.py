from copy import deepcopy
from quopri import decodestring

class User:
    pass


class Teacher(User):
    pass


class Studnet(User):
    pass

# Фабричный метод создания пользователей
class UserFactory:
    types = {
        'student': Studnet,
        'teacher': Teacher
    }
    
    @classmethod
    def create_user(cls, type_):
        return cls.types[type_]()
    

# Порождающий паттерн прототип
class CoursePrototype:
    def clone(self):
        return deepcopy(self)
    
# Модель курсов
class Course(CoursePrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.couses.append(self)
        
# Курс в записи
class RecordedCourse(Course):
    pass

# Интерактивный курс
class InteractiveCourse(Course):
    pass

# Фабричный метод создания курсов
class CourseFactory:
    types = {
        'recorded': RecordedCourse,
        'interactive': InteractiveCourse
    }
    
    @classmethod
    def create_course(cls, type_, name, category):
        return cls.types[type_](name, category)
    
# Модель категории
class Category:
    auto_id = 0
    
    def __init__(self, name, category=None):
        Category.auto_id += 1
        self.id = Category.auto_id
        self.name = name
        self.category = category
        self.courses = []
        
    def course_count(self):
        total_courses = len(self.courses)
        if self.category: 
            total_courses += self.category.corse_count()
        return total_courses
    
# Основной интерфейс
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []
        
    @staticmethod
    def create_user(type_):
        return UserFactory.create_user(type_)
    
    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)
    
    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create_course(type_, name, category)
    
    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Категории с данным идентификатором ({id}) не существует!')

    def find_course_by_name(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None
    
    @staticmethod
    def decode_value(val):
        val = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decoded = decodestring(val)
        return val_decoded.decode('UTF-8')
    
    
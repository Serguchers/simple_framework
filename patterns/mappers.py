import sqlite3
from creational_patterns import Student
from core.errors import *

connection = sqlite3.connect('test_base.sqlite')
    
# Маппер модели студента
class StudentMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'
    
    # Получение всех элементов таблицы
    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result
    
    # Поиск по id
    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')
    
    # Вставка в таблицу
    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as f:
            raise DbCommitException(f.args)
        
    # Обновление записи
    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as f:
            raise DbUpdateException(f.args)
        
    # Удаление записи
    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as f:
            raise DbDeleteException(f.args)
        

# Регистр для мапперов
class MapperRegistry:
    mappers = {
        'student': StudentMapper
    }
    
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        
    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
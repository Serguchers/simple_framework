from threading import local

# Реализация паттерна UnitOfWork
class UnitOfWork:
    current_thread = local()
    
    def __init__(self):
        self.new_objects = []
        self.objects_to_update = []
        self.removed_objects = []
        
    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry
    # Пометить объект на создание   
    def register_new(self, obj):
        self.new_objects.append(obj)
    # Пометить объект на изменение
    def register_updated(self, obj):
        self.objects_to_update.append(obj)
    # Пометить объект на удаление
    def register_removed(self, obj):
        self.removed_objects.append(obj)
        
    def commit(self):
        self.insert_new()
        self.update_object()
        self.delete_removed()
        
        self.new_objects.clear()
        self.objects_to_update.clear()
        self.removed_objects.clear()
    
    # Вставка объекта
    def insert_new(self):
        for obj in self.new_objects:
            # Получаем маппер в регистре
            self.MapperRegistry.get_mapper(obj).insert(obj)
    
    def update_object(self):
        for obj in self.objects_to_update:
            self.MapperRegistry.get_mapper(obj).update(obj)
    
    def delete_removed(self):
        for obj in self.removed_objects:
            self.MapperRegistry.get_mapper(obj).delete(obj)
    # Инициализация сессии работы с БД       
    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())
        
    @classmethod
    def set_method(cls, unit_of_work):
        cls.current_thread.unit_of_work = unit_of_work
    
    @classmethod
    def get_current(cls):
        return cls.current_thread.unit_of_work
    

class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)
        
    def mark_updated(self):
        UnitOfWork.get_current().register_updated(self)
    
    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)
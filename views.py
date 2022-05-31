from core.templator import render
from patterns.creational_patterns import Engine


site = Engine()

# class Index:
#     def __call__(self, request):
#         return '200 OK', render('index.html', date=request.get('date', None))
    

# class Contacts:
#     def __call__(self, request):
#         return '200 OK', render('contacts.html', date=request.get('date', None))
    
    
# class About:
#     def __call__(self, request):
#         return '200 OK', render('about.html', date=request.get('date', None))

# Главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)
    
# Описание проекта
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')
    

# Список курсов
class CoursesList:
    def __call__(self, request):
        try:
            # Ищем запрашиваемую категорию
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course-list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'There are no courses for this category!'
        
# Создание курсов
class CreateCourse:
    category_id = -1
    
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = site.decode_value(data['name'])
            category = None
            
            # Проверка выбрана ли уже существующая категория
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('recorded', name, category)
                site.courses.append(course)
            
            return '200 OK',render('course-list.html',
                                   objects_list=category.courses,
                                   name=category.name,
                                   id=category.id)
            
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(self.category_id)
                
                return '200 OK', render('create-course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'There is no such category!'
            
# Создание категорий
class CreateCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = site.decode_value(data['name'])
            category_id = data.get('category_id')
            category = None
            
            if category_id:
                category = site.find_category_by_id(int(category_id))
                
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            
            return '200 OK', render('index.html',
                                    object_list=site.categories)
        
        else:
            return '200 OK', render('create-category.html',
                                    categories=site.categories)
            
# Список категорий
class CategoryList:
    def __call__(self, request):
        return '200 OK', render('category-list.html',
                                objects_list=site.categories)
        
# Копирование курса
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']
        
        try:
            name = request_params['name']
            existing_course = site.find_course_by_name(name)
            if existing_course:
                new_course_name = f'copy_{name}'
                new_course = existing_course.clone()
                new_course = new_course_name
                site.courses.append(new_course)
            
            return '200 OK', render('course-list.html',
                                    objects_list=site.categories,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', 'There are no courses for this category!'          
            
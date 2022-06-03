from core.templator import render
from patterns.creational_patterns import Engine
from patterns.structural_patterns import AppRoute, TimeLogger
from patterns.observers import Subject, SmsNotifier, EmailNotifier
from patterns.class_based_views import TemplateView, ListView, CreateView
from patterns.serializers import BaseSerializer
# from urls import routes

site = Engine()
notifier = Subject()
notifier.observers = [EmailNotifier(), SmsNotifier()]
routes = {}

# Главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @TimeLogger(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)
    
# Описание проекта
@AppRoute(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')
    

# Список курсов
@AppRoute(routes=routes, url='/courses-list/')
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
@AppRoute(routes=routes, url='/create-course/')
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
@AppRoute(routes=routes, url='/create-category/')
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
            
        
# Копирование курса
@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']
        
        try:
            name = request_params['name']
            existing_course = site.find_course_by_name(name)
            if existing_course:
                category = existing_course.category
                new_course_name = f'copy_{name}'
                new_course = existing_course.clone()
                new_course.name = new_course_name
                site.courses.append(new_course)
                category.courses.append(new_course)
                
            return '200 OK', render('course-list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', 'There are no courses for this category!'          
            
            
@AppRoute(routes=routes, url='/students-list/')
class StudentsListView(ListView):
    queryset = site.students
    template_name = 'students-list.html'
    
    
@AppRoute(routes=routes, url='/create-student/')
class CreateStudentView(CreateView):
    template_name = 'create-student.html'
    
    def create_obj(self, data):
        name = site.decode_value(data['name'])
        new_student = site.create_user('student', name)
        site.students.append(new_student)
        
        
@AppRoute(routes=routes, url='/enroll-student/')
class EnrollStudentView(CreateView):
    template_name = 'enroll-student.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context
    
    def create_obj(self, data):
        course_name = site.decode_value(data['course_name'])
        course = site.find_course_by_name(course_name)
        student_name = site.decode_value(data['student_name'])
        student = site.find_student_by_name(student_name)
        course.enroll_student(student)
        notifier.notify(site)
        
        
@AppRoute(routes=routes, url='/api/')
class CourseApi:
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
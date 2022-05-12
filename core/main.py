import os
import sys
sys.path.append(os.path.dirname(__file__))

from errors import PageNotFound404
from front_controller import user_language, current_date

class Framework:
    
    def __init__(self, routes):
        self.routes = routes
        self.fronts = [user_language, current_date]
        
    def __call__(self, environ, start_response):
        # Получаем адрес, запрошенный пользователем
        path = environ['PATH_INFO']
        print(path)
        if not path.endswith('/'):
            path = f'{path}/'
        
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()
        
        # Наполняем объект request общими данными
        # для всех запросов
        request = {}
        for front in self.fronts:
            front(request)
        
        print(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
import os
import sys
sys.path.append(os.path.dirname(__file__))

import quopri
from errors import PageNotFound404
from front_controller import user_language, current_date
from requests_handler import GetRequestHandler, PostRequestHandler

class Framework:
    
    def __init__(self, routes):
        self.routes = routes
        self.fronts = [user_language, current_date]
        
    def __call__(self, environ, start_response):
        # Получаем адрес, запрошенный пользователем
        path = environ['PATH_INFO']
        
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
            
        method = environ['REQUEST_METHOD']
        request['method'] = method
        if method == 'POST':
            data = PostRequestHandler().get_request_params(environ)
            print(f'Поступил POST-запрос {Framework.decode_value(data)}')
        if method == 'GET':
            data = GetRequestHandler().get_request_params(environ)
            print(f'Поступил GET-запрос: {Framework.decode_value(data)}')
        
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
    
    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
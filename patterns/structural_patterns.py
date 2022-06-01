from time import time


class AppRoute:
    def __init__(self, routes, url):
        # Передаем ссылку на словарь с путями и url
        self.routes = routes
        self.url = url
    
    def __call__(self, cls):
        # Добавляем в словарь связь url и класса обработчика
        self.routes[self.url] = cls()
        

class TimeLogger:

    def __init__(self, name):
        self.name = name

    def __call__(self, method):
        def timeit(*args, **kwargs):
            start = time()
            result = method(*args, **kwargs)
            end = time()
            delta = end - start

            print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
            return result

        return timeit
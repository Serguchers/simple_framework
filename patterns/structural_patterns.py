class AppRoute:
    def __init__(self, routes, url):
        # Передаем ссылку на словарь с путями и url
        self.routes = routes
        self.url = url
    
    def __call__(self, cls):
        # Добавляем в словарь связь url и класса обработчика
        self.routes[self.url] = cls()
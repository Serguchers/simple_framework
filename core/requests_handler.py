def parse_input_data(data):
        result = {}
        if data:
            req_params = data.split('&')
            for param in req_params:
                k, v = param.split('=')
                result[k] = v
        return result


# Обработчик GET-запросов
class GetRequestHandler:

    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = parse_input_data(query_string)
        return request_params
    

# Обработчик POST-запросов
class PostRequestHandler:
    
    @staticmethod
    def get_wsgi_input_data(environ):
        # Получаем длину тела запроса
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        # Считываем данные
        data = environ['wsgi.input'].read(content_length) if content_length else b''
        return data
    
    
    @staticmethod
    def get_request_params(environ):
        data = PostRequestHandler.get_wsgi_input_data(environ)
        if data:
            data_str = data.decode(encoding='utf-8')
            data = parse_input_data(data_str)
        return data
    
from email.mime import application
from wsgiref.simple_server import make_server
from core.main import Framework
from urls import routes


application = Framework(routes)


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()

from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
from os.path import join


def render(tmplt_name, folder='templates', **kwargs):
    
    # Объект окружения
    env = Environment()
    # Устанавливаем loader, который будет искать шаблоны в папке
    env.loader = FileSystemLoader(folder)
    template = env.get_template(tmplt_name)
    
    return template.render(**kwargs)
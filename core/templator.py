from jinja2 import Template
from os.path import join


def render(tmplt_name, folder='templates', **kwargs):
    file_path = join(folder, tmplt_name)
    with open(file_path, encoding='utf-8') as page:
        template = Template(page.read())
    return template.render(**kwargs)
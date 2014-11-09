from jinja2 import Environment, FileSystemLoader
import sys
import os
import json

try:
    TEMPLATE_DIRS = json.loads(os.environ['TEMPLATE_DIRS'])
except KeyError, e:
    TEMPLATE_DIRS = [os.path.join(path, 'templates') for path in sys.path]


env = Environment(loader=FileSystemLoader(TEMPLATE_DIRS))


def parseRequest(request):
    return {}


def page(request, template_name, context):
    data = parseRequest(request)
    data.update(context)
    template = env.get_template(template_name)
    html = template.render(**data)
    if isinstance(html, unicode):
        return html.encode('utf-8')
    return html

from neji.resource import Resource, File, root
from neji.shortcuts import page
from os import path


class Home(Resource):

    def render_GET(self, request):
        return page(request, 'home.html', {})


class HelloWorld(Resource):

    def render_GET(self, request):
        return page(request, 'hello.html', {})


root.putChild('', Home())
root.putChild('static', File(path.join(path.dirname(__file__), 'static')))
root.putChild('hello', HelloWorld())

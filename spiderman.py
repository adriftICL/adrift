#!env/bin/python

from random import randint
from types import ClassType
from collections import defaultdict as ddict
import web

urls = []
handlers = ddict(lambda: ClassType("",(),{})) # XXX: constructing nameless classes...

class method(object):
    def __init__(self, method, url):
        self.method = method
        self.url = url
        self.handler = handlers[url]
    def __call__(self, func):
        def get_response(self, *args, **kwargs):
            response = func(*args, **kwargs) or "default for " + func.__name__
            return response
        self.handler.__dict__[self.method] = get_response
        urls.append(self.url)
        urls.append(self.handler)

class get(method):
    def __init__(self, url):
        super(get, self).__init__("GET", url)

class post(method):
    def __init__(self, url):
        super(get, self).__init__("POST", url)

def run():
    web.application(urls).run()

def haml(self):
    import haml
    from web.contrib.template import render_mako
    render = render_mako(directories=['views'], preprocessor=haml.preprocessor)

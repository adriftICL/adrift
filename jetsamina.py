import web

# TODO: move this and url handling to spiderman class
import haml
from web.contrib.template import render_mako
render = render_mako(directories=['views'], preprocessor=haml.preprocessor)

urls = (
        '/', 'map',
    )

class map:
    def GET(self):
        return render.map();

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

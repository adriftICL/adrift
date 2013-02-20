import web

# TODO: move this and url handling to spiderman class
import haml
from web.contrib.template import render_mako
render = render_mako(directories=['views'], preprocessor=haml.preprocessor)

urls = (
        '/', 'map',
        '/example/\((.*), (.*)\)', 'run',
    )

class map:
    def GET(self):
        return render.map()

class run:
    def GET(self, lat, lng):
        print "GOT:", lat + ", " + lng

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

#!env/bin/python

import web
import haml
import mako.lookup
import json
from tracer import run_tracer, is_landpoint, get_closest_index, is_lacking_data
from cache import get_cached_results, NotCached, cache_results, NotWritten
from logging import getLogger, INFO, Formatter
from logging.handlers import TimedRotatingFileHandler

haml_lookup = mako.lookup.TemplateLookup(directories=["views"], preprocessor=haml.preprocessor)
def render_haml(filename, **args):
    return haml_lookup.get_template(filename).render(**args)

urls = ('/fukushima', 'Fukushima',
        '/deepwaterhorizon', 'DeepWaterHorizon',
        '/rubberduckiespill', 'RubberDuckieSpill',
        '/renaspill', 'RenaSpill',
        '/', 'Index',
        '/favicon.ico', 'Favicon',
        '/map', 'Map',
        '/run', 'RunTracer',
        '/australia', 'Australia',
        '/runAus','RunTracerAus',
        '/what', 'What',
        '/what_haml', 'What_haml',
        '/how', 'How',
        '/how_haml', 'How_haml',
        '/background', 'Background',
        '/background_haml', 'Background_haml',
        '/faq', 'FAQ',
        '/faq_haml', 'FAQ_haml',
        '/media', 'Media',
        '/media_haml', 'Media_haml',
        '/team', 'Team',
        '/team_haml', 'Team_haml')

# set up logging. for more information, see
# http://docs.python.org/2/howto/logging.html#logging-basic-tutorial

logger = getLogger(__name__)
logger.propagate = False

handler = TimedRotatingFileHandler("log/adrift.log", when="D", interval=1)
formatter = Formatter("%(asctime)s,%(message)s", datefmt='%m/%d/%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(INFO)

# dedicated experiments

class Fukushima:
    def GET(self):
        logger.info(str(web.ctx.ip) + " fukushima")
        return render_haml('map.haml', lat=37.8, lng=142, centre=141.0, icon_filename="MarkerTsunami.png", open_page="")

class DeepWaterHorizon:
    def GET(self):
        logger.info(str(web.ctx.ip) + " deepwaterhorizon")
        return render_haml('map.haml', lat=28, lng=-89.4, centre=-70.0, icon_filename="MarkerOilRig.png", open_page="")

class RubberDuckieSpill:
    def GET(self):
        logger.info(str(web.ctx.ip) + " rubberduckiespill")
        return render_haml('map.haml', lat=44.7, lng=178.1, centre=-165, icon_filename="MarkerDuckie.png", open_page="")

class RenaSpill:
    def GET(self):
        logger.info(str(web.ctx.ip) + " renaspill")
        return render_haml('map.haml', lat=-37.5, lng=176.7, centre=-140, icon_filename="MarkerShip.png", open_page="")

# other pages

class Index:
    def GET(self):
        logger.info(str(web.ctx.ip) + " root")
        return render_haml('map.haml', icon_filename="MarkerDuckie.png", open_page="")

class Map:
    def GET(self):
        i = web.input()
        try:
            try:
                centre = i.centre
            except AttributeError:
                centre = 30
            return render_haml('map.haml', lat=i.lat, lng=i.lng, centre=centre, icon_filename="MarkerDuckie.png", open_page="")
        except AttributeError:
            return render_haml('map.haml', icon_filename="MarkerDuckie.png", open_page="")

class Favicon:
    def GET(self):
        raise web.redirect("/static/favicon.ico")

class RunTracer:
    def GET(self):
        i = web.input()
        try:
            given_lat = float(i.lat)
            given_lng = float(i.lng)
        except AttributeError:
            # if no attributes are given, return nothing.
            return ""

        logger.info(str(web.ctx.ip) + " map," + str(given_lat) + "," + str(given_lng))

        closest_index = get_closest_index(given_lat, given_lng,'Global')

        ret = ""

        if is_lacking_data(closest_index,'Global'):
            ret = json.dumps("Sorry, we have no data for that ocean area")
        elif is_landpoint(closest_index,'Global'):
            ret = json.dumps("You clicked on land, please click on the ocean")
        else:
            try:
                results = get_cached_results(closest_index,'Global')
            except NotCached:
                results = run_tracer(closest_index,'Global')
                try:
                    cache_results(closest_index, results,'Global')
                except NotWritten:
                    print "Not saving data"

            web.header("Content-Type", "application/x-javascript")

            ret = json.dumps(results)

        return ret

class What:
    def GET(self):
        logger.info(str(web.ctx.ip) + " what")
        return render_haml('map.haml', icon_filename="MarkerDuckie.png", open_page="what_haml")
class What_haml:
    def GET(self):
        return render_haml('what.haml')

class How:
    def GET(self):
        logger.info(str(web.ctx.ip) + " how")
        return render_haml('map.haml', icon_filename="MarkerDuckie.png", open_page="how_haml")
class How_haml:
    def GET(self):
        return render_haml('how.haml')

class Background:
    def GET(self):
        logger.info(str(web.ctx.ip) + " background")
        return render_haml('map.haml', icon_filename="MarkerDuckie.png", open_page="background_haml")
class Background_haml:
    def GET(self):
        return render_haml('background.haml')

class FAQ:
    def GET(self):
        logger.info(str(web.ctx.ip) + " faq")
        return render_haml('map.haml', icon_filename="MarkerDuckie.png", open_page="faq_haml")
class FAQ_haml:
    def GET(self):
        return render_haml('faq.haml')

class Team:
    def GET(self):
        logger.info(str(web.ctx.ip) + " team")
        return render_haml('map.haml', icon_filename="MarkerDuckie.png", open_page="team_haml")
class Team_haml:
    def GET(self):
        return render_haml('team.haml')

class Media:
    def GET(self):
        logger.info(str(web.ctx.ip) + " media")
        return render_haml('map.haml', icon_filename="MarkerDuckie.png", open_page="media_haml")
class Media_haml:
    def GET(self):
        return render_haml('media.haml')

class Australia:
    def GET(self):
        i = web.input()
        try:
            return render_haml('australia.haml', lat=i.lat, lng=i.lng, icon_filename="MarkerDuckie.png", open_page="")
        except AttributeError:
            return render_haml('australia.haml', icon_filename="MarkerDuckie.png", open_page="")
class RunTracerAus:
    def GET(self):
        i = web.input()
        try:
            given_lat = float(i.lat)
            given_lng = float(i.lng)
        except AttributeError:
            # if no attributes are given, return nothing.
            return ""
        logger.info(str(web.ctx.ip) + " australia," + str(given_lat) + "," + str(given_lng))
        closest_index = get_closest_index(given_lat, given_lng,'Australia')
        ret = ""
        if is_lacking_data(closest_index,'Australia'):
            ret = json.dumps("Sorry, we have no data for that ocean area")
        elif is_landpoint(closest_index,'Australia'):
            ret = json.dumps("You clicked on land, please click on the ocean")
        else:
            try:
                results = get_cached_results(closest_index,'Australia')
            except NotCached:
                results = run_tracer(closest_index,'Australia')
                try:
                    cache_results(closest_index, results,'Australia')
                except NotWritten:
                    print "Not saving data"

            web.header("Content-Type", "application/x-javascript")
            ret = json.dumps(results)
        return ret

def notfound():
    return web.notfound(render_haml('map.haml', icon_filename="MarkerDuckie.png"))

if __name__ == "__main__":
    from sys import argv
    if not (len(argv) >= 2 and argv[1].startswith("dev")):
        web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    else:
        argv.pop(1)
    app = web.application(urls,globals())
    app.notfound = notfound
    app.run()

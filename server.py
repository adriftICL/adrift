#!env/bin/python

import web
import json
from tracer import run_tracer, is_landpoint, get_closest_index, is_lacking_data
from cache import get_cached_results, NotCached, cache_results, NotWritten
from logging import getLogger, INFO, Formatter
from logging.handlers import TimedRotatingFileHandler

urls = ('/fukushima', 'Fukushima',
        '/deepwaterhorizon', 'DeepWaterHorizon',
        '/rubberduckiespill', 'RubberDuckieSpill',
        '/renaspill', 'RenaSpill',
        '/', 'Index',
        '/favicon.ico', 'Favicon',
        '/map', 'Map',
        '/run', 'RunTracer',
        '/backward', 'Backward',
        '/runBwd', 'RunTracerBwd',
        '/australia', 'Australia',
        '/runAus','RunTracerAus',
        '/mediterranean', 'Mediterranean',
        '/runMed','RunTracerMed',
        '/klokhuis','Klokhuis',
        '/runKlok','RunTracerKlok',
        '/what', 'What',
        '/how', 'How',
        '/background', 'Background',
        '/faq', 'FAQ',
        '/media', 'Media',
        '/team', 'Team',
        '/plastinography','Plastinography',
        '/regions', 'Regions',
        '/bwdfwd','BwdFwd')

render = web.template.render('templates', base='map_layout')
servemap750 = web.template.render('templates', base='map750_layout')
render675 = web.template.render('templates', base='map675_layout')

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
        return render.map(lat=37.8, lng=142, center=141.0, icon_filename="/static/MarkerTsunami.png")

class DeepWaterHorizon:
    def GET(self):
        logger.info(str(web.ctx.ip) + " deepwaterhorizon")
        return render.map(lat=28, lng=-89.4, center=-70.0, icon_filename="/static/MarkerOilRig.png")

class RubberDuckieSpill:
    def GET(self):
        logger.info(str(web.ctx.ip) + " rubberduckiespill")
        return render.map(lat=44.7, lng=178.1, center=-165)

class RenaSpill:
    def GET(self):
        logger.info(str(web.ctx.ip) + " renaspill")
        return render.map(lat=-37.5, lng=176.7, center=-140, icon_filename="/static/MarkerShip.png")

# other pages

class Index:
    def GET(self):
        logger.info(str(web.ctx.ip) + " root")
        return render.map()

class Map:
    def GET(self):
        i = web.input()
        try:
            try:
                center = i.center
            except AttributeError:
                center = 30
            return render.map(lat=i.lat, lng=i.lng, center=center)
        except AttributeError:
            return render.map()

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
            linkfile = "https://swift.rc.nectar.org.au:8888/v1/AUTH_24efaa1ca77941c18519133744a83574/globalCsv/Global_index"+str(closest_index).zfill(5)+".csv";
            ret = json.dumps(linkfile)

        return ret

class What:
    def GET(self):
        logger.info(str(web.ctx.ip) + " what")
        return render.map(open_page="what")

class How:
    def GET(self):
        logger.info(str(web.ctx.ip) + " how")
        return render.map(open_page="how")

class Background:
    def GET(self):
        logger.info(str(web.ctx.ip) + " background")
        return render.map(open_page="background")

class FAQ:
    def GET(self):
        logger.info(str(web.ctx.ip) + " faq")
        return render.map(open_page="faq")

class Team:
    def GET(self):
        logger.info(str(web.ctx.ip) + " team")
        return render.map(open_page="team")

class Media:
    def GET(self):
        logger.info(str(web.ctx.ip) + " media")
        return render.map(open_page="media")

class Plastinography:
    def GET(self):
        logger.info(str(web.ctx.ip) + " plastinography")
        return servemap750.map750()

class Klokhuis:
    def GET(self):
        logger.info(str(web.ctx.ip) + " klokhuis")
        return render675.map675()
class RunTracerKlok:
    def GET(self):
        i = web.input()
        try:
            given_lat = float(i.lat)
            given_lng = float(i.lng)
        except AttributeError:
            # if no attributes are given, return nothing.
            return ""

        logger.info(str(web.ctx.ip) + " klokhuis," + str(given_lat) + "," + str(given_lng))

        closest_index = get_closest_index(given_lat, given_lng,'Global')

        ret = ""

        if is_lacking_data(closest_index,'Global'):
            ret = json.dumps("Sorry, we hebben geen data voor die locatie")
        elif is_landpoint(closest_index,'Global'):
            ret = json.dumps("Sorry, je klikte niet op de oceaan")
        else:
            linkfile = "https://swift.rc.nectar.org.au:8888/v1/AUTH_24efaa1ca77941c18519133744a83574/globalCsv/Global_index"+str(closest_index).zfill(5)+".csv";
            ret = json.dumps(linkfile)

        return ret

class Regions:
    def GET(self):
        logger.info(str(web.ctx.ip) + " regions")
        return render.map(open_page="regions")

class BwdFwd:
    def GET(self):
        logger.info(str(web.ctx.ip) + " bwdfwd")
        return render.map(open_page="bwdfwd")

class Australia:
    def GET(self):
        i = web.input()
        try:
            return render.australia(lat=i.lat, lng=i.lng)
        except AttributeError:
            return render.australia()
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
            linkfile = "https://swift.rc.nectar.org.au:8888/v1/AUTH_24efaa1ca77941c18519133744a83574/australiaCsv/Australia_index"+str(closest_index).zfill(5)+".csv";
            ret = json.dumps(linkfile)

        return ret

class Mediterranean:
    def GET(self):
        i = web.input()
        try:
            return render.mediterranean(lat=i.lat, lng=i.lng)
        except AttributeError:
            return render.mediterranean()
class RunTracerMed:
    def GET(self):
        i = web.input()
        try:
            given_lat = float(i.lat)
            given_lng = float(i.lng)
        except AttributeError:
            # if no attributes are given, return nothing.
            return ""
        logger.info(str(web.ctx.ip) + " mediterranean," + str(given_lat) + "," + str(given_lng))
        closest_index = get_closest_index(given_lat, given_lng,'Mediterranean')
        ret = ""
        if is_lacking_data(closest_index,'Mediterranean'):
            ret = json.dumps("Sorry, we have no data for that ocean area")
        elif is_landpoint(closest_index,'Australia'):
            ret = json.dumps("You clicked on land, please click on the ocean")
        else:
            linkfile = "https://swift.rc.nectar.org.au:8888/v1/AUTH_24efaa1ca77941c18519133744a83574/MediterraneanCsv/Mediterranean_index"+str(closest_index).zfill(5)+".csv";
            ret = json.dumps(linkfile)

        return ret

class Backward:
    def GET(self):
        i = web.input()
        try:
            try:
                center = i.center
            except AttributeError:
                center = 30
            return render.backward(lat=i.lat, lng=i.lng, center=center)
        except AttributeError:
            return render.backward()
class RunTracerBwd:
    def GET(self):
        i = web.input()
        try:
            given_lat = float(i.lat)
            given_lng = float(i.lng)
        except AttributeError:
            # if no attributes are given, return nothing.
            return ""
        logger.info(str(web.ctx.ip) + " backward," + str(given_lat) + "," + str(given_lng))
        closest_index = get_closest_index(given_lat, given_lng,'GlobalBwd')
        ret = ""
        if is_lacking_data(closest_index,'GlobalBwd'):
            ret = json.dumps("Sorry, we have no data for that ocean area")
        elif is_landpoint(closest_index,'GlobalBwd'):
            ret = json.dumps("You clicked on land, please click on the ocean")
        else:
            linkfile = "https://swift.rc.nectar.org.au:8888/v1/AUTH_24efaa1ca77941c18519133744a83574/globalbwdCsv/Global_index"+str(closest_index).zfill(5)+".csv";
            ret = json.dumps(linkfile)

        return ret

def notfound():
    return web.notfound(render.map())


if __name__ == "__main__":
    from sys import argv
    if not (len(argv) >= 2 and argv[1].startswith("dev")):
        web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    else:
        argv.pop(1)
    app = web.application(urls,globals())
    app.notfound = notfound
    app.run()

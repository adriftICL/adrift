#!env/bin/python

from spiderman.helpers import *
import json
from tracer import run_tracer, is_landpoint, get_closest_index, is_lacking_data
from cache import get_cached_results, NotCached, cache_results, NotWritten
from logging import getLogger, INFO, Formatter
from logging.handlers import TimedRotatingFileHandler

# set up logging. for more information, see
# http://docs.python.org/2/howto/logging.html#logging-basic-tutorial

logger = getLogger(__name__)
logger.propagate = False

handler = TimedRotatingFileHandler("log/adrift.log", when="D", interval=1)
formatter = Formatter("%(asctime)s,%(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(INFO)

# dedicated experiments

@get('/fukushima')
def map(): return haml(lat=37.8, lng=141.0, centre=141.0)

@get('/sydney')
def map(): return haml(lat=-33.8, lng=151.2, centre=151.2)

# other pages

@get('/')
def under_construction(): return haml()

@get('/map')
def map():
    i = web.input()
    try:
        try:
            centre = i.centre
        except AttributeError:
            centre = 30
        return haml(lat=i.lat, lng=i.lng, centre=centre)
    except AttributeError:
        return haml()

@get('/favicon.ico')
def favicon(): raise web.redirect("/static/favicon.ico")

# api

@get('/run')
def doit():
    i = web.input()
    try:
        given_lat = float(i.lat)
        given_lng = float(i.lng)
    except AttributeError:
        # if no attributes are given, return nothing.
        return ""

    logger.info(str(web.ctx.ip) + "," + str(given_lat) + "," + str(given_lng))

    closest_index = get_closest_index(given_lat, given_lng)

    ret = ""

    if is_lacking_data(closest_index):
        ret = json.dumps("Sorry, we have no data for that ocean area")
    elif is_landpoint(closest_index):
        ret = json.dumps("You clicked on land, please click on the ocean")
    else:
        try:
            results = get_cached_results(closest_index)
        except NotCached:
            results = run_tracer(closest_index)
            try:
                cache_results(closest_index, results)
            except NotWritten:
                print "Not saving data"

        web.header("Content-Type", "application/x-javascript")

        ret = json.dumps(results)

    return ret

@get('/what')
def what(): pass

@get('/how')
def how(): pass

@get('/background')
def background(): pass

@get('/team')
def team(): pass

run()

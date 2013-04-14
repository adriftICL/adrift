#!env/bin/python

from spiderman.helpers import *
import json
from tracer import run_tracer, is_landpoint, get_closest_index, is_lacking_data
from cache import get_cached_results, NotCached, cache_results

SHOULD_CACHE = True

@get('/')
def under_construction(): return haml()

@get('/map')
def map():
    i = web.input()
    try:
        return haml(lat=i.lat, lng=i.lng)
    except AttributeError:
        return haml()

@get('/favicon.ico')
def favicon(): raise web.redirect("/static/favicon.ico")

@get('/run/\((.*),(.*)\)')
def doit(given_lat, given_lng):
    given_lat = float(given_lat)
    given_lng = float(given_lng)
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
            if SHOULD_CACHE:
                cache_results(closest_index, results)

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

#!env/bin/python

from spiderman.helpers import *
import json
from tracer import run_tracer, is_landpoint, get_closest_index, is_lacking_data
from cache import get_cached_results, NotCached, cache_results

@get('/')
def under_construction(): return haml()

@get('/map')
def map():
    i = web.input()
    try:
        return haml(lat=i.lat, lng=i.lng, centre=i.centre)
    except AttributeError:
        return haml()

@get('/favicon.ico')
def favicon(): raise web.redirect("/static/favicon.ico")

@get('/run')
def doit():
    i = web.input()
    try:
        given_lat = float(i.lat)
        given_lng = float(i.lng)
    except AttributeError:
        given_lat = -1.1
        given_lng = 117.8

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

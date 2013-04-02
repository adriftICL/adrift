#!env/bin/python

from spiderman.helpers import *

import scipy.io
import json
from scipy import *

data = scipy.io.loadmat('data/tracerappdata.mat')
P = data['P'][0]
coastp = data['coastp']
popdens = data['popdens']
lon = data['lon'][0]
landpoints = data['landpoints'][0]
lat = data['lat'][0]

@get('/')
def under_construction(): haml()

@get('/map')
def map(): haml()

@get('/\((.*),\s*(.*)\)')
def map(lat, lng): return haml(**locals()) # locals lat and lng automatically passed to template

@get('/favicon.ico')
def favicon(): raise web.redirect("/static/favicon.ico")

@get('/run/\((.*),\s*(.*)\)')
def run_tracer(given_lat, given_lng):
    given_lat = float(given_lat)
    given_lng = float(given_lng)

    maxyears = 2

    v = zeros((1,P[0].shape[0]))

    def find(array, value, mod):
        best = 9999 + abs(value)
        best_i = -1
        for i in xrange(len(array)):
            for delta in [-mod,0,+mod]:
                if abs(array[i]-value+delta) < best:
                    best = abs(array[i]-value+delta)
                    best_i = i
        return best_i

    closest_index = find(lat, given_lat, 0) * len(lon) + find(lon, given_lng, 360)

    v[0][closest_index] = 1

    ret = ""

    if landpoints[closest_index] == -1:
        ret = json.dumps("Sorry, we have no data for that ocean area")
    elif landpoints[closest_index] == -1:
        ret = json.dumps("You clicked on land, please click on the ocean")
    else:
        results = []

        def extract_important_points(v):
            heatMapData = []
            index = 0
            for i in lat:
                for j in lon:
                    if v[0][index] > 1e-4:
                        heatMapData.append({'location': {'lat':int(i),'lng':int(j)}, 'weight': v[0][index]})
                    index += 1
            return heatMapData

        for y in xrange(maxyears):
            for bm in P:
                v = v * bm
                results.append(extract_important_points(v))

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

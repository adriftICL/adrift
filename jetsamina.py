#!env/bin/python

from spiderman.helpers import *

import scipy.io
import cPickle as pickle
import os
import json
from scipy import *

try:
      data = scipy.io.loadmat('data/tracerappdata.mat')
except IOError as e:
      print("({})".format(e))
      print
      print "Error: You need to get the tracerappdata.mat file first. It then goes in ./data/"
      print "       Contact Erik van Sebille (mailto: e.vansebille@unsw.edu.au) for this."
      print
      exit()

P = data['P'][0]
coastp = data['coastp']
popdens = data['popdens']
lon = data['lon'][0]
landpoints = data['landpoints'][0]
lat = data['lat'][0]

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
def run_tracer(given_lat, given_lng):
    given_lat = float(given_lat)
    given_lng = float(given_lng)

    maxyears = 10
    minplotval = 1e-4

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
    
    filename='SavedReqs/closest_index' +str(closest_index).zfill(5)

    ret = ""

    if landpoints[closest_index] == -1:
        ret = json.dumps("Sorry, we have no data for that ocean area")
    elif landpoints[closest_index] == +1:
        ret = json.dumps("You clicked on land, please click on the ocean")
    else:
        if os.path.exists(filename):
            results=pickle.load(open(filename,"rb"))
        else:
            results = []
            def extract_important_points(v):
                heatMapData = []
                index = 0
                for i in lat:
                    for j in lon:
                        if v[0][index] > minplotval:
                            vval = int(min(v[0][index]*10000,100))
                            heatMapData.append({'location': {'lat':int(i),'lng':int(j)}, 'weight': vval})
                        index += 1
                return heatMapData

            for y in xrange(maxyears):
                  for bm in P:
                      v = v * bm
                      results.append(extract_important_points(v))
        
            pickle.dump(results,open(filename,"wb"))
        
        
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

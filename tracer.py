#!env/bin/python

import scipy.io
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

def is_landpoint(closest_index):
    return landpoints[closest_index] == +1

def is_lacking_data(closest_index):
    return landpoints[closest_index] == -1

def get_closest_index(given_lat, given_lng):
    def find(array, value, mod):
        best = 9999 + abs(value)
        best_i = -1
        for i in xrange(len(array)):
            for delta in [-mod,0,+mod]:
                if abs(array[i]-value+delta) < best:
                    best = abs(array[i]-value+delta)
                    best_i = i
        return best_i
    return find(lat, given_lat, 0) * len(lon) + find(lon, given_lng, 360)

def run_tracer(closest_index):
    maxyears = 10
    minplotval = 1e-4

    v = zeros((1, P[0].shape[0]))

    v[0][closest_index] = 1

    results = []

    def extract_important_points(v):
        heatMapData = []
        index = 0
        for i in lat:
            for j in lon:
                if v[0][index] > minplotval:
                    vval = int(min(v[0][index]*10000, 100))
                    heatMapData.append({'location': {'lat':int(i),'lng':int(j)}, 'weight': vval})
                index += 1
        return heatMapData

    for y in xrange(maxyears):
          for bm in P:
              v = v * bm
              results.append(extract_important_points(v))

    return results

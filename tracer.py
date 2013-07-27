#!env/bin/python

import scipy.io
from scipy import *

try:
      dataGlobal = scipy.io.loadmat('data/tracerappdataGlobal.mat')
      dataAustralia = scipy.io.loadmat('data/tracerappdataAustralia.mat')
except IOError as e:
      print("({})".format(e))
      print
      print "Error: You need to get the tracerappdata*.mat files first. It then goes in ./data/"
      print "       Contact Erik van Sebille (mailto: e.vansebille@unsw.edu.au) for this."
      print
      exit()

PGlobal = dataGlobal['P'][0]
lonGlobal = dataGlobal['lon'][0]
landpointsGlobal = dataGlobal['landpoints'][0]
latGlobal = dataGlobal['lat'][0]

PAustralia = dataAustralia['P'][0]
lonAustralia = dataAustralia['lon'][0]
landpointsAustralia = dataAustralia['landpoints'][0]
latAustralia = dataAustralia['lat'][0]
nxAustralia = dataAustralia['nx'][0]
nyAustralia = dataAustralia['ny'][0]
lonAustralia = lonAustralia[0:nxAustralia[0]]
latAustralia = latAustralia[0:nyAustralia[0]]

def is_landpoint(closest_index,type):
    if type=='Global':
        return landpointsGlobal[closest_index] == +1
    if type=='Australia':
        return landpointsAustralia[closest_index] == +1

def is_lacking_data(closest_index,type):
    if type=='Global':
        return landpointsGlobal[closest_index] == -1
    if type=='Australia':
        return landpointsAustralia[closest_index] == -1

def get_closest_index(given_lat, given_lng,type):
    def find(array, value, mod):
        best = 9999 + abs(value)
        best_i = -1
        for i in xrange(len(array)):
            for delta in [-mod,0,+mod]:
                if abs(array[i]-value+delta) < best:
                    best = abs(array[i]-value+delta)
                    best_i = i
        return best_i
    if type=='Global':
        return find(latGlobal, given_lat, 0) * len(lonGlobal) + find(lonGlobal, given_lng, 360)
    if type=='Australia':
        return find(latAustralia, given_lat, 0) * len(lonAustralia) + find(lonAustralia, given_lng, 360)

def run_tracer(closest_index,type):
    if type=='Global':
        P=PGlobal
        lat=latGlobal
        lon=lonGlobal
        maxyears=10
        minplotval=2.5e-4
    if type=='Australia':
        P=PAustralia
        lat=latAustralia
        lon=lonAustralia
        maxyears=3
        minplotval=1e-4,

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

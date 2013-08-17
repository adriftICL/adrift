#!env/bin/python

import scipy.io
from scipy import *

data={}
try:
      data['Global'] = scipy.io.loadmat('data/tracerappdataGlobal.mat')
      data['Australia'] = scipy.io.loadmat('data/tracerappdataAustralia.mat')
except IOError as e:
      print("({})".format(e))
      print
      print "Error: You need to get the tracerappdata*.mat files first. It then goes in ./data/"
      print "       Contact Erik van Sebille (mailto: e.vansebille@unsw.edu.au) for this."
      print
      exit()

lon = {}
lat = {}
lon['Global']=data['Global']['lon'][0]
lat['Global']=data['Global']['lat'][0]
nx = data['Australia']['nx'][0]
ny = data['Australia']['ny'][0]
lon['Australia']=data['Australia']['lon'][0][0:nx[0]]
lat['Australia']=data['Australia']['lat'][0][0:ny[0]]

def is_landpoint(closest_index,type):
    return data[type]['landpoints'][0][closest_index] == +1

def is_lacking_data(closest_index,type):
    return data[type]['landpoints'][0][closest_index] == -1

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
    return find(lat[type], given_lat, 0) * len(lon[type]) + find(lon[type], given_lng, 360)

def run_tracer(closest_index,type):
    if type=='Global':
        maxyears=10
        minplotval=2.5e-4
    if type=='Australia':
        maxyears=5
        minplotval=1e-4,

    v = zeros((1, data[type]['P'][0][0].shape[0]))

    v[0][closest_index] = 1

    results = []

    def extract_important_points(v):
        heatMapData = []
        index = 0
        for i in lat[type]:
            for j in lon[type]:
                if v[0][index] > minplotval:
                    vval = int(min(v[0][index]*10000, 100))
                    heatMapData.append({'location': {'lat':int(i),'lng':int(j)}, 'weight': vval})
                index += 1
        return heatMapData

    for y in xrange(maxyears):
          for bm in data[type]['P'][0]:
              v = v * bm
              results.append(extract_important_points(v))

    return results

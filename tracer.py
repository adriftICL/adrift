#!env/bin/python

import scipy.io
from scipy import *
import time

data={}
try:
      data['Global'] = scipy.io.loadmat('data/tracerappdataGlobal.mat')
      data['GlobalBwd'] = scipy.io.loadmat('data/tracerappdataGlobalBwd.mat')
      data['Australia'] = scipy.io.loadmat('data/tracerappdataAustralia.mat')
      data['Mediterranean'] = scipy.io.loadmat('data/tracerappdataMediterranean.mat')
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
lon['GlobalBwd']=data['GlobalBwd']['lon'][0]
lat['GlobalBwd']=data['GlobalBwd']['lat'][0]
nx = data['Australia']['nx'][0]
ny = data['Australia']['ny'][0]
lon['Australia']=data['Australia']['lon'][0][0:nx[0]]
lat['Australia']=data['Australia']['lat'][0][0:ny[0]]
nx = data['Mediterranean']['nx'][0]
ny = data['Mediterranean']['ny'][0]
lon['Mediterranean']=data['Mediterranean']['lon'][0][0:nx[0]]
lat['Mediterranean']=data['Mediterranean']['lat'][0][0:ny[0]]

def is_landpoint(closest_index,type):
    return data[type]['landpoints'][0][closest_index] == +1

def is_lacking_data(closest_index,type):
    return data[type]['landpoints'][0][closest_index] == -1

def get_closest_index(given_lat, given_lng,type):
    def findindex(array, value):
        diffs=abs(array-value) % 360
        return diffs.argmin()
    return findindex(lat[type], given_lat) * len(lon[type]) + findindex(lon[type], given_lng)

# this function is not to be used anymore!!
def run_tracer(closest_index,type):
    if type=='Global':
        maxyears=10
        minplotval=2.5e-4
    if type=='GlobalBwd':
        maxyears=10
        minplotval=2.5e-4
    if type=='Australia':
        maxyears=5
        minplotval=1e-4,
    if type=='Mediterranean':
        maxyears=3
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
                    heatMapData.append({'location': {'lat':int(i*10)/10.,'lng':int(j*10)/10.}, 'weight': vval})
                index += 1
        return heatMapData

    for y in xrange(maxyears):
          for bm in data[type]['P'][0]:
              v = v * bm
              results.append(extract_important_points(v))

    return results

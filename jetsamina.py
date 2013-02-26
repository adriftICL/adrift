import web

# TODO: move this and url handling to spiderman class
import haml
from web.contrib.template import render_mako
render = render_mako(directories=['views'], preprocessor=haml.preprocessor)

urls = (
        '/', 'map',
        '/run/\((.*), (.*)\)', 'run',
    )

class map:
    def GET(self):
        return render.map()


import scipy.io
import json
from scipy import *

def doit(given_lat, given_lon):
    data = scipy.io.loadmat('data/tracerappdata.mat')
    P = data['P'][0]
    coastp = data['coastp']
    popdens = data['popdens']
    lon = data['lon'][0]
    landpoints = data['landpoints']
    lat = data['lat'][0]

    maxyears = 10

    v = zeros((1,P[0].shape[0]))

    def find(array, value):
        best = 9999 + abs(value)
        best_i = -1
        for i in xrange(len(array)):
            if abs(array[i]-value) < best:
                best = abs(array[i]-value)
                best_i = i
        return best_i
        
    v[0][find(lat, given_lat) * len(lon) + find(lon, given_lon)] = 1

    for y in xrange(maxyears):
        for bm in P:
            v = v * bm

    heatMapData = []

    index = 0
    for j in lon:
        for i in lat:
            if v[0][index] > 1e-7:
                heatMapData.append({'location': {'lat':int(i),'lng':int(j)}, 'weight': v[0][index]})
            index += 1

    return json.dumps(heatMapData)


class run:
    def GET(self, lat, lng):
        return doit(float(lat), float(lng))

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

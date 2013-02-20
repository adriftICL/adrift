#load('tracerappdata.mat')

# Just a quick benchmark :) takes one argument: the number of years to run the tracer.

import scipy.io
import numpy
from scipy import *

data = scipy.io.loadmat('data/tracerappdata.mat')
P = data['P'][0]
coastp = data['coastp']
popdens = data['popdens']
lon = data['lon'][0]
landpoints = data['landpoints']
lat = data['lat'][0]

#   maxyears=100;

import sys
maxyears = int(sys.argv[1])

#   %Initializing
#   v=zeros(1,size(P{1},1));

v = zeros((1,P[0].shape[0]))

#   %choose either the release of garbage along all world coastlines
#   % v(coastp)=popdens/sum(popdens);
#   %or choose a particular location (such as Sydney)
#   v(sub2ind([numel(lon),numel(lat)],154, 45))=1;

#v[0][153 * len(lat) + 44] = 1
v[0][44 * len(lon) + 153] = 1

#   %add white to the color bar so that we can see the continents
#   colormap('default')
#   map = colormap;
#   map=cat(1,[1 1 1],map);
#   colormap(map);

#   for y=1:maxyears;
#     for bm=1:6
#       % The vector-matrix multiplication
#       v=v*P{bm};

for y in xrange(maxyears):
    for bm in P:
        v = v * bm

#       
#       % plotting
#       vplot=v;
#       vplot(landpoints==1)=NaN;
#       imagesc(lon,lat,reshape(vplot,numel(lon),numel(lat))',[-1e-4 1e-3])
#       axis xy
#       title(['Tracer after ',num2str(y),' years and ',num2str((bm-1)*2),' months'])
#       drawnow
#     end
#   end

if maxyears == 100:
    output = scipy.io.loadmat('data/output_evs.mat')
    expected_v = output["v"][0]
    if sum(v-expected_v) != 0:
        print "The script is wrong..."

#!env/bin/python

from tracer import run_tracer, is_landpoint, is_lacking_data
import cPickle as pickle
from os import utime
import subprocess
import contextlib
from random import shuffle
from sys import argv
from bz2 import BZ2File

## Will raise NotCached if not readable/writable (I think..)
CACHE_ROOTGLOBAL = "cached_requests"
CACHE_ROOTAUS = "cached_requestsAus"

# open_func = BZ2File
open_func = open

class NotCached(Exception):
    pass
class NotWritten(Exception):
    pass

def get_filename(closest_index,type):
    if type=='Global':
        return CACHE_ROOTGLOBAL + '/closest_index' + str(closest_index).zfill(5)
    if type=='Australia':
        return CACHE_ROOTAUS + '/closest_index' + str(closest_index).zfill(5)

def get_cached_results(closest_index,type):
    try:
        filename = get_filename(closest_index,type)
        utime(filename, None)
        with contextlib.closing( open_func(filename, "rb")) as handle:
          return pickle.load(handle)
    except OSError:
        raise NotCached()

def cache_results(closest_index, results,type):
    try:
        with contextlib.closing( open_func(get_filename(closest_index,type), "wb")) as handle:
          pickle.dump(results, handle)
    except:
        raise NotWritten()

# Caching all data
if __name__ == "__main__":
    print "populating cache with all entries"
    entries = []
    type='Global'
    for closest_index in xrange(165 * 360):
        if not (is_landpoint(closest_index,type) or is_lacking_data(closest_index,type)):
            entries.append(closest_index)
    for closest_index in entries:
        print "  |--> processing closest index #" + str(closest_index)
        cache_results(closest_index, run_tracer(closest_index),type)

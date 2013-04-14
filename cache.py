#!env/bin/python

from tracer import run_tracer
import cPickle as pickle
from os import utime

from sys import argv

class NotCached(Exception):
    pass

def get_filename(closest_index):
    return 'SavedReqs/closest_index' + str(closest_index).zfill(5)

def get_cached_results(closest_index):
    try:
        filename = get_filename(closest_index)
        utime(filename, None)
        return pickle.load(open(filename, "rb"))
    except OSError:
        raise NotCached()

def cache_results(closest_index, results):
    pickle.dump(results, open(get_filename(closest_index), "wb"))

if __name__ == "__main__":
    print "populating cache"
    for closest_index in xrange(165 * 360):
        print "  |--> processing closest index #" + str(closest_index)
        cache_results(closest_index, run_tracer(closest_index))

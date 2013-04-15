#!env/bin/python

from tracer import run_tracer, is_landpoint, is_lacking_data
import cPickle as pickle
from os import utime
import subprocess
from random import shuffle
from sys import argv
from bz2 import BZ2File

## Will raise NotCached if not readable/writable (I think..)
CACHE_ROOT = "cached_requests"
NUMTOSAVE = "15001"

# open_func = BZ2File
open_func = open

class NotCached(Exception):
    pass
class NotWritten(Exception):
    pass

def get_filename(closest_index):
    return CACHE_ROOT + '/closest_index' + str(closest_index).zfill(5)

def get_cached_results(closest_index):
    try:
        filename = get_filename(closest_index)
        utime(filename, None)
        return pickle.load(open_func(filename, "rb"))
    except OSError:
        raise NotCached()

def cache_results(closest_index, results):
    try:
        pickle.dump(results, open_func(get_filename(closest_index), "wb"))
    except:
        raise NotWritten()
    subprocess.call(['bash','./delete_stale_saved_reqs.sh', CACHE_ROOT, NUMTOSAVE])

# This takes around 20 GB zipped, 150 GB not zipped
# TODO: compress cache
if __name__ == "__main__":
    print "populating cache with 15k random entries"
    entries = []
    for closest_index in xrange(165 * 360):
        if not (is_landpoint(closest_index) or is_lacking_data(closest_index)):
            entries.append(closest_index)
    shuffle(entries)
    entries = entries[:15000] # only 15k entries...
    for closest_index in entries:
        print "  |--> processing closest index #" + str(closest_index)
        cache_results(closest_index, run_tracer(closest_index))

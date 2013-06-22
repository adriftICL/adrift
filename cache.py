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
CACHE_ROOT = "cached_requests"
NUMTOSAVE = "40001"

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
        with contextlib.closing( open_func(filename, "rb")) as handle:
          return pickle.load(handle)
    except OSError:
        raise NotCached()

def cache_results(closest_index, results):
    try:
        with contextlib.closing( open_func(get_filename(closest_index), "wb")) as handle:
          pickle.dump(results, handle)
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
    entries = entries[:40000] # only 40k entries...
    for closest_index in entries:
        print "  |--> processing closest index #" + str(closest_index)
        cache_results(closest_index, run_tracer(closest_index))

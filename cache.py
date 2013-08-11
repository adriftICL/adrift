#!env/bin/python

from tracer import run_tracer, is_landpoint, is_lacking_data
import cPickle as pickle
import config
from random import shuffle

import boto.s3.connection
from boto.s3.key import Key
connection = boto.s3.connection.S3Connection(
          aws_access_key_id=config.aws_access_key_id,
          aws_secret_access_key=config.aws_secret_access_key,
          port=8888,
          host='swift.rc.nectar.org.au',
          is_secure=True,
          validate_certs=False,
          calling_format=boto.s3.connection.OrdinaryCallingFormat()
        )
#buckets = connection.get_all_buckets()
#botokey['Australia'] = Key(buckets[0])
bucket = [connection.get_bucket('global'),connection.get_bucket('australia')]
botokey={}
botokey['Global']=Key(bucket[0])
botokey['Australia']=Key(bucket[1])


class NotCached(Exception):
    pass
class NotWritten(Exception):
    pass

def get_filename(closest_index,type):
    return type + 'Closest_index' + str(closest_index).zfill(5)

def get_cached_results(closest_index,type):
    botokey[type].key = get_filename(closest_index,type)
    if botokey[type].exists():
        return pickle.loads(botokey[type].get_contents_as_string())
    else:
        raise NotCached()

def cache_results(closest_index, results,type):
    try:
        botokey[type].key = get_filename(closest_index,type)
        return botokey[type].set_contents_from_string(pickle.dumps(results,pickle.HIGHEST_PROTOCOL))
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
        cache_results(closest_index, run_tracer(closest_index,type),type)

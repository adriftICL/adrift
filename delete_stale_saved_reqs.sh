#!/bin/bash

cache_path="$1"

ls -t $cache_path/closest_index* | tail -n+1001 | xargs rm

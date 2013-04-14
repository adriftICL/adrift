#!/bin/bash

ls -t SavedReqs/closest_index* | tail -n+1001 | xargs rm

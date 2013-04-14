#!/bin/bash

echo i got called
ls -t SavedReqs/closest_index* | tail -n+1001 | xargs rm

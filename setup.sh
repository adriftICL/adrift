#!/bin/bash

cd $(dirname "${BASH_SOURCE[0]}")
if ! [ -e env ]
then
    virtualenv env || virtualenv2 env
fi
. env/bin/activate
which python
which pip
pwd
pip install -r requirements.txt

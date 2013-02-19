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

echo -e "The environment has been created and is up to date."
echo -e "Use it by sourcing env/bin/activate (type \033[34;1msource $(pwd)/env/bin/activate\033[0m)"

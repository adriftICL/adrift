#!/bin/bash

cd $(dirname "${BASH_SOURCE[0]}")
if ! [ -e env ]
then
    virtualenv env || virtualenv2 env
fi
. env/bin/activate
pip install numpy
if pip install -r requirements.txt
then
    echo -e "The environment has been created and is up to date."
    echo -e "Use it by sourcing env/bin/activate (type \033[34;1msource $(pwd)/env/bin/activate\033[0m)"
else
    echo -e "If there were errors installing scipy, please ensure libatlas or blas + lapack are installed."
    echo -e "On arch linux, this is \033[34;1msudo pacman -S blas lapack\033[0m"
    # TODO: add ubuntu instructions then add both to this script.
fi

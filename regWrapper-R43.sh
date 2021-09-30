#!/bin/bash

localDir=`pwd`/
currTime=`date '+%Y%m%d-%H%M%S-'`

function usage() {
    echo
    echo "Do regression rest (Python version 2.x)."
    echo "Usage: $0 <config file>"
    echo
    echo "Example:"
    echo "    ./regWrapper.sh HMC2-M257.cfg"
    echo
}

if [ $# -gt 0 ]; then
    # output the unittest trace to both screen and log file
    /usr/bin/python -Wignore ./src/regression_R43.py $localDir$1 2>&1 | tee $currTime${1%.*}.log
else
    usage
    exit 2
fi

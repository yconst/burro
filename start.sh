#!/bin/sh -

DIR="$( cd "$( dirname "$0" )" && pwd )"

if  [[ $1 = "-r" ]]; then
    sudo $DIR/../bin/python $DIR/burro/drive.py --record
else
    sudo $DIR/../bin/python $DIR/burro/drive.py
fi

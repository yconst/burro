#!/bin/sh -

DIR="$( cd "$( dirname "$0" )" && pwd )"
sudo $DIR/../bin/python $DIR/burro/drive.py --model=$DIR/burro/models/default.h5

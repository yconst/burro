#!/bin/sh -

DIR="$( cd "$( dirname "$0" )" && pwd )"
sudo $DIR/../bin/python $DIR/src/drive.py --model=$DIR/src/models/default.h5

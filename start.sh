#!/bin/sh -

DIR="$( cd "$( dirname "$0" )" && pwd )"
RECORD=false

while getopts ":r" opt; do
  case $opt in
    r)
      RECORD=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

if [ $RECORD = true ]; then
	sudo $DIR/../bin/python $DIR/burro/drive.py --record
else
	sudo $DIR/../bin/python $DIR/burro/drive.py
fi
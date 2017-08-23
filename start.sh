#!/bin/sh -

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
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
	sudo $SCRIPT_DIR/../bin/python $SCRIPT_DIR/burro/drive.py --record
else
	sudo $SCRIPT_DIR/../bin/python $SCRIPT_DIR/burro/drive.py
fi

#!/bin/bash -

while getopts "d:" opt; do
  case $opt in
    d)
      path=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -n $path ];
then
  SCRIPT_DIR=$(dirname "$SCRIPT")
  DATA_DIR=$(realpath $path)
  $SCRIPT_DIR/../bin/python $SCRIPT_DIR/burro/view.py --data-dir $DATA_DIR
else
  echo "Data directory argument is required" >&2
  exit 1
fi

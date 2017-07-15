#!/bin/bash -

while getopts "d:n:" opt; do
  case $opt in
    d)
      path=$OPTARG
      ;;
    n)
      name=$OPTARG
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

if [ -n $path ] && [ -n $name ];
then
  DIR="$( cd "$( dirname "$0" )" && pwd )"
  $DIR/env/bin/python $DIR/burro/train.py --data-dir $DIR/$path --model-name $name
else
  echo "Data directory and model name arguments are required" >&2
  exit 1
fi

#!/bin/sh -

while getopts "d:n:" opt; do
  case $opt in
    d)
      $path = $OPTARG"
      ;;
    n)
      $name = $OPTARG"
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

DIR="$( cd "$( dirname "$0" )" && pwd )"
sudo $DIR/../bin/python $DIR/burro/train.py --data-dir $path --name $name

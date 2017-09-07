#!../env/bin/python

"""
train.py

Trains a model

Usage:
    train.py --data-dir <dir> --model-name <name> --mode <mode>

Options:
  --data-dir <dir>      data directory
  --model-name <name>   model name
  --mode <mode>         either regression or categorical [default:regression]
"""

import sys
import time

from docopt import docopt

import methods
import config

from trainers import train_categorical, train_regression

def main():
    arguments = docopt(__doc__)
    data_dir = arguments['--data-dir']
    model_name = arguments['--model-name']
    mode = arguments['--mode']
    if mode == 'regression':
        train_regression(data_dir, model_name)
    elif mode == 'categorical':
        train_categorical(data_dir, model_name)

if __name__ == "__main__":
    main()

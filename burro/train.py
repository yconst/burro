#!../env/bin/python

"""
train.py

Trains a model

Usage:
    train.py --data-dir <DIR>, --model-name <NAME>, [--mode <MODE>]

Options:
  --data-dir <DIR>      data directory
  --model-name <NAME>   model name
  --mode <MODE>         either regression or categorical [default: categorical]
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

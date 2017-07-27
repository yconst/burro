#!../env/bin/python

"""
train.py

Trains a model

Usage:
    train.py --data-dir <dir> --model-name <name>

Options:
  --data-dir <dir>      data directory
  --model-name <name>   model name
"""

import sys
import time

from docopt import docopt

import methods
import config

from trainers import train

def main():
    arguments = docopt(__doc__)
    data_dir = arguments['--data-dir']
    model_name = arguments['--model-name']
    train(data_dir, model_name)

if __name__ == "__main__":
    main()

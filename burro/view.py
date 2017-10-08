#!../env/bin/python

"""
view.py

View resulting images of a generator pipeline

Usage:
    view.py --data-dir <DIR>, [--mode <MODE>]

Options:
  --data-dir <DIR>      data directory
  --mode <MODE>         either regression or categorical [default: categorical]
"""

import sys
import time

from docopt import docopt

import methods
import config

from trainers.img_pipelines import categorical_pipeline, regression_pipeline
from trainers.generators.pil_generators import show_image


def main():
    arguments = docopt(__doc__)
    data_dir = arguments['--data-dir']
    mode = arguments['--mode']
    if mode == 'regression':
        pipeline = regression_pipeline(data_dir, val_every=0, batch_size=1)
    elif mode == 'categorical':
        pipeline = categorical_pipeline(data_dir, val_every=0, batch_size=1)
    show_image(pipeline)


if __name__ == "__main__":
    main()

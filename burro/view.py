#!../env/bin/python

"""
view.py

View resulting images of a generator pipeline

Usage:
    view.py --data-dir <dir>

Options:
  --data-dir <dir>      data directory
"""

import sys
import time

from docopt import docopt

import methods
import config

from trainers.helpers import regression_pipeline
from trainers.generators.pil_generators import show_image


def main():
    arguments = docopt(__doc__)
    data_dir = arguments['--data-dir']
    pipeline = regression_pipeline(data_dir, val_every=0, batch_size=1)
    show_image(pipeline)


if __name__ == "__main__":
    main()

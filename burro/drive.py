"""
drive.py

Starts a driving loop

Usage:
    drive.py [--vision=<name>]

Options:
  --vision=<name>     vision sensor type [default: camera]
"""

from docopt import docopt
from rover import Rover
from composers import Composer

if __name__ == "__main__":
    arguments = docopt(__doc__)
    vision_type = arguments['--vision']
    rover = Rover()
    rover.run()

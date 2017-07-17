"""
drive.py

Starts a driving loop

Usage:
    drive.py [--record]

Options:
  --record     record images to disk [default: False]
"""

from docopt import docopt
from rover import Rover
from composers import Composer

if __name__ == "__main__":
    arguments = docopt(__doc__)
    composer = Composer()
    rover = composer.new_vehicle()
    #rover.record = arguments.record
    rover.run()

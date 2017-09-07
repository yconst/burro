import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from trainer import train_categorical, train_regression

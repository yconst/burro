import sys
import os
from glob import glob

def list_models():
    '''
    Return a list with the paths and names of all
    models in the current dir.
    '''
    file = sys.modules[__name__].__file__
    path = os.path.dirname(os.path.realpath(file))
    model_paths = glob(os.path.join(path, "*.h5"))
    return [(model_path, (os.path.basename(model_path)).capitalize()) for model_path in model_paths]

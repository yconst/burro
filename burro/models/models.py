import sys
import os


def list_models(self):
    '''
    Return a list with the paths and names of all
    models in the current dir.
    '''
    path = sys.modules[__name__].__file__
    model_paths = glob(os.path.join(path, "*.h5"))
    return [model_path, (os.path.basename(model_path)).capitalize() for model_path in model_paths]

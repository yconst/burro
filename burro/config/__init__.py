from configobj import ConfigObj

def config2object(config):
    """
    Convert dictionary into instance allowing access to dictionary keys using
    dot notation (attributes).
    """
    class ConfigObject(dict):
        """
        Represents configuration options' group, works like a dict
        """
        def __init__(self, *args, **kwargs):
            dict.__init__(self, *args, **kwargs)
        def __getattr__(self, name):
            return self[name]
        def __setattr__(self, name, val):
            self[name] = val
    if isinstance(config, dict):
        result = ConfigObject()
        for key in config:
            result[key] = config2object(config[key])
        return result
    else:
        return config

config_dict = ConfigObj('defaults.ini', unrepr=True)
user_dict = ConfigObj('user.ini', unrepr=True, create_empty=True)
config_dict.merge(user_dict)
config = config2object(config_dict)

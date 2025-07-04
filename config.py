import json
import os
from io import StringIO


class Configuration(object):
    _config = {}
    filepath = ''

    def __init__(self, filepath):
        self.filepath = filepath

        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump({}, f)

        with open(self.filepath, 'r') as f:
            self._config = json.load(f)

    def __getattr__(self, item):
        if item not in super().__getattribute__('_config'):
            return getattr(super(), item, None)
        return self._config[item]

    def __setattr__(self, key, value):
        if key in super().__dir__():
            super().__setattr__(key, value)
        else:
            self._config[key] = value

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self._config, f)


config = Configuration('config.json')
logging_io = StringIO()

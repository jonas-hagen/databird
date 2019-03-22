from dict_recursive_update import recursive_update
from frozendict import frozendict
from ruamel.yaml import YAML
import collections
import glob
import os


_settings = {}


class Settings(collections.UserDict):
    """Combine multiple mappings for sequential lookup.
    """

    def __init__(self, base_config_file):
        self._maps = {}
        self.data = frozendict()
        self._base_config = base_config_file
        base_config = self.add_file(base_config_file)
        if "includes" in base_config:
            root = os.path.dirname(base_config_file)
            for inc in base_config["includes"]:
                if not os.path.isabs(inc):
                    inc = os.path.normpath(os.path.join(root, inc))
                for fn in glob.glob(inc):
                    self.add_file(fn)

    def __setitem__(self, key, value):
        raise TypeError("immutable")

    def add_file(self, fn):
        yaml = YAML(typ="safe")
        with open(fn) as doc:
            config = yaml.load(doc)
        self._maps[fn] = config
        self.data = self.collect()
        return config

    def recursive_update(self, other):
        self.data = recursive_update(self.data, other)

    def collect(self):
        merged = {}
        for m in self._maps.values():
            merged = recursive_update(merged, m)
        return frozendict(merged)


def get_settings():
    return _settings


def initialize(base_config):
    global _settings
    _settings = Settings(base_config)

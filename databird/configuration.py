from dict_recursive_update import recursive_update
from frozendict import frozendict
from ruamel.yaml import YAML
import collections
import glob
import os
from databird import Repository
from databird import Profile
import importlib


_settings = {}


class ConfigurationError(ValueError):
    pass


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
        self.data = self.parse()

    def __setitem__(self, key, value):
        raise TypeError("immutable")

    def add_file(self, fn):
        yaml = YAML(typ="safe")
        with open(fn) as doc:
            config = yaml.load(doc)
        self._maps[fn] = config
        return config

    def _collect(self):
        merged = {}
        for m in self._maps.values():
            merged = recursive_update(merged, m)
        return frozendict(merged)

    def parse(self):
        config = self._collect()

        # Drivers
        driver_names = []
        for name, profile in config["profiles"].items():
            if "driver" not in profile:
                raise ConfigurationError(
                    "Profile {} is missing driver field.".format(name)
                )
            driver_names.append(profile["driver"])

        drivers = {}
        for name in driver_names:
            parts = name.split(".")
            package_name = ".".join(parts[:-1])
            class_name = parts[-1]
            module_name = "databird_drivers." + package_name
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError:
                raise ConfigurationError(
                    "Driver module not found: '{}' for driver '{}'".format(
                        module_name, name
                    )
                )
            try:
                drivers[name] = getattr(module, class_name)
            except AttributeError:
                raise ConfigurationError(
                    "Driver module '{}' has no class '{}'.".format(
                        module_name, class_name
                    )
                )

        # Profiles
        if "profiles" in config:
            for name, profile_config in config["profiles"].items():
                profile_config["driver"] = drivers[profile_config["driver"]]
                config["profiles"][name] = Profile(name, **profile_config)

        # Repositories
        if "repositories" in config:
            for name, repo_config in config["repositories"].items():
                if not "profile" in repo_config:
                    raise ConfigurationError(
                        "Repository `{}` is missing profile field.".format(name)
                    )
                repo_config["profile"] = config["profiles"][repo_config["profile"]]
                config["repositories"][name] = Repository(name, **repo_config)

        return config


def get_settings():
    return _settings


def initialize(base_config):
    global _settings
    _settings = Settings(base_config)

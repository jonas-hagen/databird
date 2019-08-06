from abc import ABC
import os
from dict_recursive_update import recursive_update
import tempfile
import os
import shutil


class BaseDriver(ABC):
    def __init__(self, config):
        """Create a driver with profile and repository configuration."""
        config = recursive_update(self.default_config(), config)
        self.check_config(config)

        # The _config variables will never be changed
        self._config = config

    @classmethod
    def check_config(cls, config):
        assert isinstance(config, dict)

    @classmethod
    def default_config(cls):
        return {}

    @staticmethod
    def create_dir(target):
        os.makedirs(os.path.dirname(target), exist_ok=True)

    def check_connection(self):
        """Check if connection can be established. Must not mutate self!"""
        return True

    def is_available(self, context):
        """Check if data is available for certain context. Must not mutate self!"""
        pass

    def retrieve_safe(self, context, targets):
        """Safe-copy wrapper for retrieve. Must not be overridden."""
        with tempfile.TemporaryDirectory(prefix="db_") as tempdir:
            temp_targets = {k: os.path.join(tempdir, k + ".tmp") for k in targets}
            retval = self.retrieve(context, temp_targets)
            # now copy safely to real targets
            for name in targets:
                source = temp_targets[name]
                temp_dest = targets[name] + "~"
                dest = targets[name]
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(source, temp_dest)
                os.rename(temp_dest, dest)
        return retval

    def retrieve(self, context, targets):
        """Retrieve data for certain context and different `targets`. Must not mutate self!"""
        for name, target in targets.items():
            self.retrieve_single(context, target, name)

    def retrieve_single(self, context, target, name=""):
        """Retrieve data for certain context and save as `target`. Must not mutate self!"""
        pass

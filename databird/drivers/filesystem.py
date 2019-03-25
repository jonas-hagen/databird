"""
Simple databird driver that uses a file system. Mainly used for testing.
"""
import os
import shutil
from databird import BaseDriver


class FilesystemDriver(BaseDriver):
    @classmethod
    def check_repo_config(cls, config):
        super().check_repo_config(config)
        assert "patterns" in config
        assert isinstance(config["patterns"], dict)

    @classmethod
    def check_profile_config(cls, config):
        super().check_profile_config(config)
        assert "root" in config

    def check_connection(self):
        return os.isdir(self._profile_config["root"])

    def render_filename(self, context, target_name):
        return self._repo_config["patterns"][target_name].format(**context)

    def render_abs_filename(self, context, target_name):
        source = os.path.normpath(
            os.path.join(
                self._profile_config["root"], self.render_filename(context, target_name)
            )
        )
        return source

    def is_available(self, context):
        for target_name in self._repo_config["patterns"].keys():
            if os.path.isfile(self.render_abs_filename(context, target_name)):
                return True
        return False

    def retrieve(self, context, targets):
        for name, target in targets.items():
            source = self.render_abs_filename(context, name)
            self.create_dir(target)
            shutil.copyfile(source, target)
        return True

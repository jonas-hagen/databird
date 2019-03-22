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
        assert "pattern" in config

    @classmethod
    def check_profile_config(cls, config):
        super().check_profile_config(config)
        assert "root" in config

    def check_connection(self):
        return os.isdir(self._profile_config["root"])

    def render_filename(self, context):
        return self._repo_config["pattern"].format(**context)

    def render_abs_filename(self, context):
        source = os.path.normpath(
            os.path.join(self._profile_config["root"], self.render_filename(context))
        )
        return source

    def is_available(self, context):
        return os.path.isfile(self.render_abs_filename(context))

    def retrieve(self, context, target):
        source = self.render_abs_filename(context)
        shutil.copyfile(source, target)
        return True

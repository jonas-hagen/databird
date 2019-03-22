"""
Simple databird driver that uses a file system. Mainly used for testing.
"""
import os
import shutil


class FilesystemDriver:
    def __init__(self, profile_config, repo_config):
        self.check_repo_config(repo_config)
        self.check_profile_config(profile_config)

        # The _*_config variables will never be changed
        self._profile_config = profile_config
        self._repo_config = repo_config

    @staticmethod
    def check_repo_config(config):
        assert "pattern" in config

    @staticmethod
    def check_profile_config(config):
        assert "root" in config

    def check(self):
        """Check connection."""
        return True

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

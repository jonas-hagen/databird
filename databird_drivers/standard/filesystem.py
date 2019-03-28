"""
Simple databird driver that uses a file system. Mainly used for testing.
"""
import os
import shutil
from databird import BaseDriver


class FilesystemDriver(BaseDriver):
    """
    Simple driver to retrieve data files from a local file system by copying.

    Configuration options:
      - root: The root directory where the data resides.
      - patterns: A target_name->pattern map.
          This map specifies a pattern (that is rendered in context) for every
          target name in the repository.

    Example configuration:
    ```
    root: /data/something/
    patterns:
      header: headertext_{time:%Y-%m-%d}.txt
      data: binarylog_{time:%Y-%m-%d}.bin
      code: taball_{time:%Y-%m-%d}.tar
    ```
    """

    @classmethod
    def check_config(cls, config):
        super().check_config(config)
        assert "patterns" in config
        assert isinstance(config["patterns"], dict)
        assert "root" in config

    def check_connection(self):
        return os.isdir(self._profile_config["root"])

    def render_filename(self, context, target_name):
        return self._config["patterns"][target_name].format(**context)

    def render_abs_filename(self, context, target_name):
        source = os.path.normpath(
            os.path.join(
                self._config["root"], self.render_filename(context, target_name)
            )
        )
        return source

    def is_available(self, context):
        for target_name in self._config["patterns"].keys():
            if os.path.isfile(self.render_abs_filename(context, target_name)):
                return True
        return False

    def retrieve_single(self, context, target, name):
        source = self.render_abs_filename(context, name)
        self.create_dir(target)
        return shutil.copyfile(source, target)

from databird import BaseDriver
import logging
import os
import subprocess
import shutil

logger = logging.getLogger("databird_drivers.command")


class CommandDriver(BaseDriver):
    """
    Execute a shell command to retrieve files.

    Configuration options:
    - command: The command to call (absolute path is preferred)
    - check: Check if exit status is 0
    - env: A key -> value map for environment variables to export
    - patterns: A target_name->[param list] map.
        This map specifies a pattern (that is rendered in context) for every
        target name in the repository.

    Example configuration:
    ```
    command: nsck
    check: True
    env:
      API_KEY: aa73efdd9
    patterns:
      merra_temperature:
      - "-v lat,lon,time,lev,T"
      - "https://goldsmr5.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2I3NPASM.5.12.4/{time:%Y}/{time:%m}/MERRA2_400.inst3_3d_asm_Np.{time:%Y%m%d}.nc4"
      - "{target_file}"
    ```
    """

    @classmethod
    def check_config(cls, config):
        super().check_config(config)
        assert "command" in config
        assert isinstance(config["check"], bool)
        assert isinstance(config["env"], dict)
        assert "patterns" in config
        assert isinstance(config["patterns"], dict)
        for v in config["patterns"].values():
            assert isinstance(v, list)

    @classmethod
    def default_config(cls):
        return {"env": dict(), "check": True}

    def check_connection(self):
        return shutil.which(self._config["command"]) is not None

    def is_available(self, context):
        return self.check_connection()

    def _render_arguments(self, context, target, name):
        pattern = self._config["patterns"][name]
        rendered = [arg.format(target_file=target, **context) for arg in pattern]
        return rendered

    def retrieve_single(self, context, target, name):
        # target is an absolute local path to a file
        self.create_dir(target)

        args = self._render_arguments(context, target, name)
        command = [self._config["command"]] + args

        env = os.environ.copy()
        env = env.update(self._config["env"])

        subprocess.run(command, env=env, check=self._config["check"])

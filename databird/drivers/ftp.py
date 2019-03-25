from databird.drivers import FilesystemDriver
from ftplib import FTP, FTP_TLS
import logging
import os

logger = logging.getLogger("databird.drivers.ftp")


class FtpDriver(FilesystemDriver):
    """
    This driver gets data from standard FTP servers. The FTP Protocol can
    be considered a legacy, but still data is distributed that way.

    Configuration options:
    - host: Host name
    - tls: Flag to enable TLS (default: false)
    - user: Username (connect anonymously if not set)
    - password: Password for user (default: '')
    - root: The base directory to change to after connect.
    - patterns: A target_name->pattern map.
        This map specifies a pattern (that is rendered in context) for every
        target name in the repository.

    Example configuration:
    ```
    host: cddis.nasa.gov
    tls: true
    user: foo
    password: bar
    root: /gnss/data/daily
    patterns:
      v3status: {time:%Y}/{time:%j}/{time:%y%j}.V3status
      status: {time:%Y}/{time:%j}/{time:%y%j}.status
    ```
    """

    @classmethod
    def check_config(cls, config):
        super().check_config(config)
        assert "host" in config

    @classmethod
    def default_config(cls):
        return {"user": "anonymous", "password": "", "tls": False}

    def _connect(self):
        if self._config["tls"]:
            c = FTP_TLS(self._config["host"])
        else:
            c = FTP(self._config["host"])
        if self._config["user"]:
            c.login(self._config["user"], self._config["password"])
        return c

    def check_connection(self):
        try:
            c = self._connect()
        except Exception as e:
            logger.error(str(e))
            return False
        else:
            c.close()
            return True

    def is_available(self, context):
        c = self._connect()
        for target_name in self._config["patterns"].keys():
            size = c.size(self.render_abs_filename(context, target_name))
            if size:
                return True
        return False

    def retrieve(self, context, targets):
        c = self._connect()
        for name, target in targets.items():
            source = self.render_abs_filename(context, name)
            source_dir = os.path.dirname(source)
            source_file = os.path.basename(source)
            self.create_dir(target)
            with open(target, "wb") as f:
                c.cwd(source_dir)
                c.retrbinary("RETR " + source_file, f.write)

        return True

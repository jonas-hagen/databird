from databird.classes import get_context
from databird_drivers.standard import FtpDriver
import datetime as dt
import pytest


@pytest.mark.external_service
def test_ftp(tmpdir):
    fd = FtpDriver(
        dict(
            host="cddis.nasa.gov",
            user="anonymous",
            password="",
            tls=False,
            root="/gnss/data/daily",
            patterns=dict(status="{time:%Y}/{time:%j}/{time:%y%j}.status"),
        )
    )
    context = get_context(time=dt.datetime(2019, 1, 11))

    target = tmpdir.join("file.status")

    # Since we are connecting a third-party service,
    # only run the test if the connection can be established
    if fd.check_connection():
        assert fd.is_available(context)

        fd.retrieve(context, dict(status=target))

        with open(target) as f:
            first_line = f.readline()
        assert first_line.startswith(
            "IGS Tracking Network Status (RINEX V2 Data) for 11-Jan-19"
        )

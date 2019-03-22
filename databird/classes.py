from importlib import import_module
from databird import dtutil
from databird import BaseDriver
from typing import List, Set, Dict, Tuple, Optional
import datetime as dt


class Profile:
    def __init__(self, name, driver: BaseDriver = None, configuration=None):
        if driver is None:
            raise ValueError("`driver` is required")
        if configuration is None:
            configuration = {}
        self.name = name
        self.driver = driver
        self.configuration = configuration

        driver.check_profile_config(configuration)


class Repository:
    def __init__(
        self,
        name: str,
        period: str = None,
        start: dt.datetime = None,
        profile: Profile = None,
        targets: List[str] = None,
        description: str = "",
        delay: str = None,
        hooks: List[str] = None,
        configuration: Dict = None,
    ):
        # Check required arguments
        if period is None:
            raise ValueError("`period` is required.")
        if start is None:
            raise ValueError("`start` is required.")
        if profile is None:
            raise ValueError("`profile` is required.")
        if targets is None:
            raise ValueError("`targets` is required.")

        # Set default values
        if delay is None:
            delay = period
        if hooks is None:
            hooks = []
        if configuration is None:
            configuration = {}

        # Parse values
        self.delay = dtutil.parse_timedelta(delay)
        self.start = start
        self.period = dtutil.parse_timedelta(period)

        self.name = name
        self.description = description

        # Instantiate the driver
        profile.driver.check_repo_config(configuration)
        self.driver = profile.driver(profile.configuration, configuration)

    def list_missing():
        """List missing targets."""
        pass

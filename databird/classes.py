from databird import BaseDriver
from databird import dtutil
from importlib import import_module
from typing import List, Set, Dict, Tuple, Optional
import datetime as dt
import os


def get_context(time):
    return {"time": time}


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
        if not targets:
            raise ValueError("`targets` is required.")

        if len(targets) > 1:
            raise NotImplementedError("more than one target.")

        # Set default values
        if delay is None:
            delay = period
        if hooks is None:
            hooks = []
        if configuration is None:
            configuration = {}

        # Parse values
        self.delay = dtutil.parse_timedelta(delay)
        self.period = dtutil.parse_timedelta(period)

        self.name = name
        self.description = description
        self.start = start
        self.targets = targets

        # Instantiate the driver
        profile.driver.check_repo_config(configuration)
        self.driver = profile.driver(profile.configuration, configuration)

    def iter_missing(self, root_dir):
        """List missing targets."""
        base_path = os.path.join(root_dir, self.name)
        end_date = dt.datetime.now() - self.delay
        print("----->", self.start, end_date, self.period)
        for time in dtutil.iter_dates(self.start, end_date, self.period):
            context = get_context(time=time)
            filename = self.targets[0].format(**context)
            target = os.path.join(base_path, filename)
            if not os.path.exists(target):
                yield context, target

    def iter_available(self, root_dir):
        for context, target in self.iter_missing(root_dir):
            if self.driver.is_available(context):
                yield context, target

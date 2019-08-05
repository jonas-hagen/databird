from databird import BaseDriver
from databird import dtutil
from databird import utils
from dict_recursive_update import recursive_update
from importlib import import_module
from typing import List, Set, Dict, Tuple, Optional
import datetime as dt
import os


class Profile:
    def __init__(self, name, driver: BaseDriver = None, configuration=None):
        if driver is None:
            raise ValueError("`driver` is required")
        if configuration is None:
            configuration = {}
        self.name = name
        self.driver = driver
        self.configuration = configuration


class Repository:
    def __init__(
        self,
        name: str,
        period: str = None,
        start: dt.datetime = None,
        profile: Profile = None,
        targets: Dict[str, str] = None,
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
        self.start = dtutil.normalize_datetime(start)
        self.targets = targets

        # Instantiate the driver
        driver_config = recursive_update(profile.configuration, configuration)
        self.driver = profile.driver(driver_config)

    def _render_targets(self, root_dir, context):
        base_path = os.path.join(root_dir, self.name)
        targets = dict()
        for name, target in self.targets.items():
            filename = target.format(**context)
            targets[name] = os.path.join(base_path, filename)
        return targets

    def hash(self, context):
        targets = self._render_targets("", context)
        return utils.hash_dict(targets)

    @staticmethod
    def _targets_reached(targets):
        """
        Check if a set of (rendered) targets is reached.

        Currently a 'set of targets' is reached if one file of the set exists.
        This is the most simple and robust way for now, but might change in future.
        """
        for target in targets.values():
            if os.path.exists(target):
                return True
        return False

    def iter_missing(self, root_dir, ref_time=None):
        """
        List missing targets.

        Specifying `ref_time` (default: now) makes this function only depend on
        the file system contents under `root_dir/repo_name`.
        """
        ref_time = ref_time or dt.datetime.now()
        end_date = ref_time - self.delay
        for time in dtutil.iter_dates(self.start, end_date, self.period):
            context = utils.get_context(time=time)
            targets = self._render_targets(root_dir, context)
            if not self._targets_reached(targets):
                yield context, targets

    def iter_available(self, root_dir):
        for context, target in self.iter_missing(root_dir):
            if self.driver.is_available(context):
                yield context, target

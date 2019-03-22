from importlib import import_module
from databird import dtutil


class Profile:
    def __init__(self, name, driver=None):
        self.name = name
        self.driver = driver


class Repository:
    def __init__(
        self,
        name,
        description="",
        period=None,
        start=None,
        delay=None,
        profile=None,
        targets=None,
        hooks=None,
        configuration=None,
    ):
        pass

from abc import ABC


class BaseDriver(ABC):
    def __init__(self, profile_config, repo_config):
        """Create a driver with profile and repository configuration."""
        self.check_repo_config(repo_config)
        self.check_profile_config(profile_config)

        # The _*_config variables will never be changed
        self._profile_config = profile_config
        self._repo_config = repo_config

    @classmethod
    def check_repo_config(cls, config):
        assert isinstance(config, dict)

    @classmethod
    def check_profile_config(cls, config):
        assert isinstance(config, dict)

    def check_connection(self):
        """Check if connection can be established."""
        return True

    def is_available(self, context):
        """Check if data is available for certain context."""
        pass

    def retrieve(self, context, target):
        """Retrieve data for certain context and save as `target` file."""
        pass

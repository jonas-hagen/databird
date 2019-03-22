from databird import configuration
import os
import pytest

CONFIG_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "files", "etc", "databird"
)


def test_settings():
    base_config = os.path.join(CONFIG_DIR, "databird.conf")
    assert os.path.exists(base_config)

    configuration.initialize(base_config)
    settings = configuration.get_settings()

    assert "general" in settings
    assert "root" in settings["general"]
    assert "profiles" in settings
    assert "repositories" in settings


def test_recursive_update():
    base_config = os.path.join(CONFIG_DIR, "databird.conf")
    configuration.initialize(base_config)
    settings = configuration.get_settings()

    assert "filesystem1" in settings["profiles"]
    assert "other" in settings["profiles"]


def test_immutability():
    base_config = os.path.join(CONFIG_DIR, "databird.conf")
    configuration.initialize(base_config)
    settings = configuration.get_settings()

    with pytest.raises(TypeError):
        settings["foo"] = "bar"
    # with pytest.raises(TypeError):
    #    settings["general"]["root"] = "laber"

import databird.blueprints as blueprints
import os
import pytest
import subprocess
import tempfile


defaults_file = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "defaults.ini"
)

blueprints_path = os.path.join(os.path.dirname(blueprints.__file__))


templates = [
    template
    for template in next(os.walk(blueprints_path))[1]
    if ".mrbob.ini" in os.listdir(os.path.join(blueprints_path, template))
]


@pytest.fixture(scope="module")
def output_dir():
    return tempfile.mkdtemp()


@pytest.mark.parametrize("template", templates)
def test_template_is_created_with_defaults_file(template, output_dir):
    check = subprocess.check_call(
        [
            "mrbob",
            "-O",
            output_dir,
            "-c",
            defaults_file,
            "-n",
            os.path.join(blueprints_path, template),
        ],
        stdout=subprocess.DEVNULL,
    )
    assert 0 == check

import yaml
import pytest
import os
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def config():
    with open(Path(f"{dir_path}/config.yml")) as conf_file:
        conf = yaml.load(conf_file, Loader=yaml.FullLoader)
        return conf

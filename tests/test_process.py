import pytest
import os
from pathlib import Path
from kelloggrs import process


dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def process_logger(config):
    return process.make_logger(config["in_path"], True)


def test_process_script(script_runner, config):
    in_path = Path(dir_path) / f"{config['in_path']}"

    ret = script_runner.run("process_pages", "-h")
    assert ret.success
    assert ret.stdout != ""
    assert ret.stderr == ""

    ret = script_runner.run("process_pages", "-v", "-f", f"{in_path}", "1,2,3", "8")
    assert ret.success

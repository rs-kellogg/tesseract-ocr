import pytest
import os
import logging
import fitz
from pathlib import Path
from kelloggrs import process


dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def process_logger(config):
    logger = logging.getLogger("cafrs")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    fh = logging.FileHandler(f"{config['out_path']}/extract.log")
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    return logger


def test_process_script(script_runner):
    ret = script_runner.run("process_pages", "-h")
    assert ret.success
    assert ret.stdout != ""
    assert ret.stderr == ""


def test_process_images(config):
    in_path = Path(dir_path) / f"../{config['in_path']}"


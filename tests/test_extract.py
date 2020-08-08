import pytest
import os
import logging
import fitz
from pathlib import Path
from kelloggrs import extract

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def extract_logger(config):
    logger = logging.getLogger("extract")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    fh = logging.FileHandler(f"{dir_path}/{config['in_path']}/extract.log")
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    return logger


def test_extract_script(script_runner, config):
    in_path = Path(dir_path) / f"{config['in_path']}"

    ret = script_runner.run("extract_pages", "-h")
    assert ret.success
    assert ret.stdout != ""
    assert ret.stderr == ""

    ret = script_runner.run("extract_pages", "-v", f"{in_path}", "1")
    assert ret.success


def test_extract_pages(config):
    in_path = Path(dir_path) / f"{config['in_path']}"
    pdf_file = in_path / config["test_pdf"]

    pages = extract.extract_pages(pdf_file)
    assert len(pages[1]) == 9

    pages = extract.extract_pages(pdf_file, page_nums={1, 2, 3})
    assert len(pages[1]) == 3

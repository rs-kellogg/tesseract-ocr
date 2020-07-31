#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys
import re
import logging
import fitz
import tempfile
from PIL import Image as IM


def extract_pages(in_path, out_path):
    for pdf_file in in_path.glob("*.pdf"):
        print(pdf_file.name)


def main():
    # parse the arguments
    parser = argparse.ArgumentParser(prog="extract_pages")
    parser.add_argument("in_path", help="the path to the input pdf files")
    parser.add_argument("out_path", help="the path to the output image files")
    parser.add_argument(
        "-v", "--verbose", help="increase verbosity", action="store_true"
    )

    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        parser.exit()

    args = parser.parse_args()

    # set up logger
    logger = logging.getLogger("extract")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh = logging.FileHandler(Path(args.out_path) / "cafrs_extract.log")
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    if args.verbose:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    extract_pages(in_path, out_path)

    sys.exit(0)


if __name__ == "__main__":
    main()

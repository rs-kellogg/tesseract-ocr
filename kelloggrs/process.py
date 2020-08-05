#!/usr/bin/env python3

import argparse
import sys
import logging
import pytesseract
from PIL import Image
from pathlib import Path
from typing import List, Set, Tuple


def process_image(image_file: Path) -> List[str]:
    ocr_texts = []
    ocr_text = pytesseract.image_to_string(
        Image.open(image_file), config=r"-l eng --psm 6 -c preserve_interword_spaces=1"
    )
    return ocr_text


def main():
    # parse the arguments
    parser = argparse.ArgumentParser(prog="process_pages")
    parser.add_argument("in_path", help="the path to the input image files")
    parser.add_argument("page_nums", help="the page numbers to extract text from")
    parser.add_argument(
        "-v", "--verbose", help="increase verbosity", action="store_true"
    )

    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        parser.exit()

    args = parser.parse_args()

    # set up logger
    logger = logging.getLogger("process")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh = logging.FileHandler(Path(args.in_path) / "process.log")
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    if args.verbose:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)

    if args.page_nums in ["all", "All", "ALL"]:
        page_nums = None
    else:
        page_nums = {int(n) for n in args.page_nums.split(",")}

    in_path = Path(args.in_path)

    subdirs = [f for f in in_path.iterdir() if f.is_dir()]
    for dir in subdirs:
        for png_file in dir.glob("*.png"):
            if page_nums:
                curr_num = int(png_file.stem.split("-")[-1])
                if curr_num not in page_nums:
                    continue
            if logger:
                logger.info(f"processing page file: {png_file.name}")
            Path(f"{dir}/{png_file.stem}.txt").write_text(process_image(png_file))

    sys.exit(0)


if __name__ == "__main__":
    main()

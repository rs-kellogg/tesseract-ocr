#!/usr/bin/env python3

import argparse
import sys
import logging
import pytesseract
import dask
from datetime import datetime as dt
from PIL import Image
from pathlib import Path
from typing import List, Set, Tuple
from dask.distributed import Client


def process_file(image_file: Path, logger) -> bool:
    try:
        logger.info(f"processing file: {image_file.name}")
        ocr_text = pytesseract.image_to_string(
            Image.open(image_file), config=r"-l eng --psm 6 -c preserve_interword_spaces=1"
        )
        Path(image_file.parent / f"{image_file.stem}.txt").write_text(ocr_text)
        return True
    except:
        return False


def main():
    # parse the arguments
    parser = argparse.ArgumentParser(prog="process_pages")
    parser.add_argument("in_path", help="the path to the input image files")
    parser.add_argument("page_nums", help="the page numbers to process")
    parser.add_argument("n_workers", help="number of workers to use")
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

    n_workers = int(args.n_workers)
    dask.config.set(scheduler='processes')
    dask.config.set(n_workers=n_workers)

    logger.info(f"processing subdirectories in path: {in_path}")
    subdirs = [f for f in in_path.iterdir() if f.is_dir()]
    for dir in subdirs:
        start = dt.now()
        process_tasks = []
        for image_file in list(dir.glob("*.png")):
            if page_nums:
                curr_num = int(image_file.stem.split("-")[-1])
                if curr_num not in page_nums:
                    continue
            process_tasks.append(dask.delayed(process_file)(image_file, logger))
        result = dask.delayed(sum)(process_tasks)
        sum_result = dask.compute(result)[0]
        end = dt.now()
        logger.info(f"{dir.name}: {sum_result} pages successfully processed in {end-start} seconds")

    sys.exit(0)


if __name__ == "__main__":
    main()

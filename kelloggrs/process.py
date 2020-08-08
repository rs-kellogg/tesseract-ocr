#!/usr/bin/env python3

import argparse
import sys
import os
import logging
import pytesseract
import dask
from datetime import datetime as dt
from PIL import Image
from pathlib import Path
from dask.distributed import Client


def remove_text_files(in_path):
    txt_files = list(in_path.rglob("*index-page-[0-9].txt"))
    for txt_file in txt_files:
        os.remove(txt_file)


def process_file(image_file: Path, overwrite: bool) -> bool:
    try:
        outfile = Path(image_file.parent / f"{image_file.stem}.txt")
        if overwrite or not (outfile.is_file()):
            ocr_text = pytesseract.image_to_string(
                Image.open(image_file),
                config=r"-l eng --psm 6 -c preserve_interword_spaces=1",
            )
            outfile.write_text(ocr_text)
        return True
    except:
        return False


def make_logger(in_path: Path, verbose: bool) -> logging.Logger:
    logger = logging.getLogger("process")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh = logging.FileHandler(in_path / "process.log")
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    if verbose:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
    return logger


def main():
    # parse the arguments
    parser = argparse.ArgumentParser(prog="process_pages")
    parser.add_argument("in_path", help="the path to the input image files")
    parser.add_argument("page_nums", help="the page numbers to process")
    parser.add_argument("n_workers", help="number of workers to use")
    parser.add_argument(
        "-v", "--verbose", help="increase verbosity", action="store_true"
    )
    parser.add_argument(
        "-f", "--force", help="over-write existing files", action="store_true"
    )
    if len(sys.argv[1:]) == 0:
        parser.print_usage()
        parser.exit()
    args = parser.parse_args()

    # determine which pages to process
    if args.page_nums in ["all", "All", "ALL"]:
        page_nums = None
    else:
        page_nums = {int(n) for n in args.page_nums.split(",")}

    in_path = Path(args.in_path)
    n_workers = int(args.n_workers)
    over_write = args.force

    # make the logger
    logger = make_logger(in_path, args.verbose)

    logger.info(f"processing image files in path: {in_path}")
    logger.info(f"page numbers to process: {args.page_nums}")
    logger.info(f"using number of workers: {n_workers}")
    logger.info(f"over-write existing files: {over_write}")

    client = Client(n_workers=n_workers)
    # dask.config.set(scheduler="multiprocessing")
    # dask.config.set(n_workers=n_workers)

    image_files = list(in_path.rglob("*index-page-[0-9].png"))
    process_tasks = []
    start = dt.now()
    # sum_result = 0
    for image_file in image_files:
        if page_nums:
            curr_num = int(image_file.stem.split("-")[-1])
            if curr_num not in page_nums:
                continue
        # sum_result += process_file(image_file, over_write)
        process_tasks.append(dask.delayed(process_file)(image_file, over_write))
    result = dask.delayed(sum)(process_tasks)
    sum_result = dask.compute(result)[0]
    end = dt.now()
    logger.info(
        f"{in_path.name}: {sum_result} pages successfully processed in {end-start} seconds"
    )

    client.close()
    sys.exit(0)


if __name__ == "__main__":
    main()

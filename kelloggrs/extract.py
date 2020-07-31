#!/usr/bin/env python3

import argparse
import sys
import logging
import fitz
import tempfile
from PIL import Image as IM
from pathlib import Path
from typing import List, Set, Tuple


def extract_pdfs(in_path: Path, out_path: Path, logger: logging.Logger = None, page_nums: Set[int] = None):
    for pdf_file in in_path.glob("*.pdf"):
        if logger:
            logger.info(f"extracting page images from pdf: {pdf_file.name}")
        doc, pages = extract_pages(pdf_file, page_nums)
        for p in pages:
            pix = p.getPixmap(fitz.Matrix(3,3))
            pix.writeImage(f"{str(out_path)}/{pdf_file.stem}-page-{p.number}.png")


def extract_pages(pdf_file: Path, page_nums: Set[int] = None) -> Tuple[fitz.Document, List[fitz.Page]]:
    doc = fitz.open(pdf_file)
    pages = list(doc.pages())
    extracted_pages = []
    if page_nums is not None:
        nums = page_nums.copy()
    else:
        nums = set(range(len(pages)))
    for p in pages:
        if p.number in nums:
            extracted_pages.append(p)
            nums.remove(p.number)
            if not nums:
                break
    return (doc, extracted_pages)

# def write_image(pdf_file: Path, out_path: Path):
#     with tempfile.TemporaryDirectory() as temp_dir:
#         try:
#             doc = fitz.open(pdf_file)
#             if doc.pageCount > 0:
#                 for p in doc.pages():
#                     pix = p.getPixmap(fitz.Matrix(2, 2))
#                     # pix = p.getPixmap(fitz.Matrix(3, 3))
#                     pix.writeImage(
#                         f"{str(temp_dir)}/{pdf_file.stem}-page-{p.number}.png"
#                     )
#                 png_files = list(Path(temp_dir).glob("*.png"))
#                 png_files.sort()
#                 images = [IM.open(png_file) for png_file in png_files]
#                 CAFRSTableExtractor.combine_images(
#                     images, out_path / f"{pdf_file.stem}.png"
#                 )
#         except Exception as e:
#             self.logger.error(f"Exception thrown on {pdf_file.name}: {e}")
#         finally:
#             pass

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
    fh = logging.FileHandler(Path(args.out_path) / "extract.log")
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
    extract_page_images(in_path, out_path, logger)

    sys.exit(0)


if __name__ == "__main__":
    main()

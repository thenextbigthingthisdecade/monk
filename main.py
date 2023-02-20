#!/usr/bin/env python3

import argparse
import logging
from collections import deque
from lexer import Tokenizer
from parser import Parser
from pprint import pprint


def run_compiler(file_path: str) -> None:
    print("Smpl(s) programming language compiler\n")
    tokens = deque()
    with open(file_path, "r") as f:
        tokenizer = Tokenizer(f.read())
        tokens = tokenizer.get_tokens()
    tree = Parser(tokens).parse()
    pprint(tree)


def setup() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-log",
        "--loglevel",
        default="warning",
        help="Provide logging level. Example --loglevel debug, default=warning",
    )
    parser.add_argument(
        "-file",
        "--filePath",
        default="sample.mnk",
        help="Provide the path to the file to be compiled, default='sample.mnk'",
    )
    args = parser.parse_args()
    return args.loglevel.upper(), args.filePath


def run_interpreter() -> None:
    print("Monk version 1.0.0")
    logging.debug("Tokenizing input file")


if __name__ == "__main__":
    level, file_path = setup()
    logging.basicConfig(format="[%(levelname)s] %(name)s - %(message)s", level=level)
    logger = logging.getLogger(__name__)
    run_compiler(file_path)

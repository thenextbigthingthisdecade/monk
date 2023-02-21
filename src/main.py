#!/usr/bin/env python3

import logging
from collections import deque
from pprint import pprint
from lexer import Tokenizer, Token
from parser import Parser
from typing import Optional
from config import level, file_path


def run_compiler(file_path: str) -> None:
    print("Monk programming language v1.0.0-alpha")
    tokens: Optional[deque[Token]] = deque()
    with open(file_path, "r") as f:
        tokenizer = Tokenizer(f.read())
        tokens = tokenizer.get_tokens()
    if not tokens:
        return
    tree = Parser(tokens).parse()
    pprint(tree)


def run_interpreter() -> None:
    print("Monk programming language v1.0.0-alpha")
    logging.debug("Tokenizing input file")


if __name__ == "__main__":
    logging.basicConfig(format="[%(levelname)s] %(name)s - %(message)s", level=level)
    logger = logging.getLogger(__name__)
    run_compiler(file_path)

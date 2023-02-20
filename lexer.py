from collections import deque
from dataclasses import dataclass
import logging
from typing import Deque
import re

lexer_logger = logging.getLogger("__main__. " + __name__)
logging.basicConfig(
    format="[%(levelname)s] %(name)s - %(message)s", level=logging.DEBUG
)


@dataclass
class Token:
    type: str = ""
    val: str = ""


class Tokenizer:
    def __init__(self, inp: str) -> None:
        self.TOKEN_TYPES = [
            ("_def", r"\bdef\b"),
            ("_end", r"\bend"),
            ("_print", r"\bprintln!"),
            ("_identifier", r"\b[a-zA-Z]+\b"),
            ("_string", r"\"[a-zA-Z{} ]+\""),
            ("_integer", r"\b\d+\b"),
            ("_oparen", r"\("),
            ("_equals", r"="),
            ("_cparen", r"\)"),
            ("_plus", r"\+"),
            ("_comma", r","),
        ]
        self.inp = inp

    def get_tokens(self) -> Deque[Token]:
        tokens = deque()
        while self.inp:
            tokens.append(self.get_one_token())
            self.inp = self.inp.strip()
        lexer_logger.debug(f"tokens from input file: {tokens}")
        return tokens

    def get_one_token(self) -> Token | None:
        for token_type, rgx in self.TOKEN_TYPES:
            match = re.match(rgx, self.inp)
            if match:
                st, end = match.span()
                val = self.inp[st:end]
                self.inp = self.inp[end:]
                token = Token(token_type, val)
                return token
        raise RuntimeError(f"Unexpected token at: {self.inp}")

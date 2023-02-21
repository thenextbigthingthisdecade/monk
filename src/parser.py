import logging
from pprint import pformat
from lexer import Token
from collections import deque
from dataclasses import dataclass, field
from config import level

parser_logger = logging.getLogger("__main__." + __name__)
logging.basicConfig(format="[%(levelname)s] %(name)s - %(message)s", level=level)


@dataclass
class Node:
    ...


@dataclass
class AssignNode(Node):
    var: Token
    expr: Node


@dataclass
class IntegerNode(Node):
    val: int


@dataclass
class VarRefNode(Node):
    val: str


@dataclass
class DefNode(Node):
    name: str
    body: list[Node] | None
    args: list[str] = field(default_factory=list)


@dataclass
class CallNode(Node):
    name: str
    args: list[str] = field(default_factory=list)


@dataclass
class PrintNode(CallNode):
    str_literal: Token = Token()


class Parser:
    def __init__(self, tokens: deque[Token]) -> None:
        self.tokens = tokens
        self.prog: list[Node] = []

    def parse(self) -> list[Node]:
        if not self.tokens:
            parser_logger.debug(f"ast for sample file: {pformat(self.prog)}")
        elif self.peek("_def"):
            fn = self.parse_def()
            self.prog.append(fn)
            self.parse()
        return self.prog

    def parse_def(self):
        _ = self.consume("_def")
        name = self.consume("_identifier").val
        args = self.parse_args()
        statements = []
        self.parse_statements(statements)
        _ = self.consume("_end")
        node = DefNode(name=name, args=args, body=statements)
        return node

    def parse_statements(self, statements: list[Node]):
        if self.peek("_end"):
            return
        if self.peek("_identifier") and self.peek("_equals", 1):
            assign_node = self.parse_assignment()
            statements.append(assign_node)
        if self.peek("_print"):
            print_node = self.parse_print()
            statements.append(print_node)
        self.parse_statements(statements)

    def parse_print(self) -> PrintNode:
        _ = self.consume("_print")
        _ = self.consume("_oparen")
        str_literal = self.consume("_string")
        # parser_logger.debug(f"value of str_literal in println! call: {str_literal}")
        _ = self.consume("_comma")
        args = self.parse_print_args()
        print_node = PrintNode(name="println!", str_literal=str_literal, args=args)
        return print_node

    def parse_print_args(self):
        args = []
        if self.peek("_identifier"):
            args.append(self.consume("_identifier").val)
            while self.peek("_comma"):
                self.consume("_comma")
                args.append(self.consume("_identifier").val)
        _ = self.consume("_cparen")
        return args

    def parse_call(self):
        name = self.consume("_identifier").val
        args = self.parse_call_args()
        node = CallNode(name=name, args=args)
        return node

    def parse_call_args(self):
        _ = self.consume("_oparen")
        args = []
        if not self.peek("_cparen"):
            args.append(self.parse_expr())
            while self.peek("_comma"):
                self.consume("_comma")
                args.append(self.parse_expr())
        _ = self.consume("_cparen")
        return args

    def parse_args(self) -> list[str]:
        _ = self.consume("_oparen")
        args = []
        if self.peek("_identifier"):
            args.append(self.consume("_identifier").val)
            while self.peek("_comma"):
                self.consume("_comma")
                args.append(self.consume("_identifier").val)
        _ = self.consume("_cparen")
        return args

    def parse_variable_ref(self):
        return VarRefNode(self.consume("_identifier").val)

    def parse_assignment(self):
        var = self.consume("_identifier")
        _ = self.consume("_equals")
        expr = self.parse_expr()
        assign_node = AssignNode(var=var, expr=expr)
        return assign_node

    def parse_expr(self):
        if self.peek("_integer"):
            return IntegerNode(int(self.consume("_integer").val))
        elif self.peek("_identifier") and self.peek("_oparen", 1):
            return self.parse_call()
        else:
            return self.parse_variable_ref()

    def consume(self, expected_type: str) -> Token:
        token = self.tokens.popleft()
        if token.type == expected_type:
            return token
        else:
            raise RuntimeError(
                f"Expected token_type: {expected_type}, got: {token.type}"
            )

    def peek(self, expected_type: str, offset: int = 0):
        return self.tokens[offset].type == expected_type

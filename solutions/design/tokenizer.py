from dataclasses import dataclass
from typing import Optional


@dataclass
class Token:
    kind: str
    value: Optional[int] = None

    def __repr__(self) -> str:
        return (
            f"Token({self.kind}, {self.value})"
            if self.value is not None
            else f"Token({self.kind})"
        )


SINGLE_CHAR = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "(": "LPAREN",
    ")": "RPAREN",
}


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    while i < len(source):
        c = source[i]
        if c.isspace():
            i += 1
        elif c.isdigit():
            j = i
            while j < len(source) and source[j].isdigit():
                j += 1
            tokens.append(Token("NUM", int(source[i:j])))
            i = j
        elif c in SINGLE_CHAR:
            tokens.append(Token(SINGLE_CHAR[c]))
            i += 1
        else:
            raise SyntaxError(f"Unexpected character {c!r} at position {i}")
    tokens.append(Token("EOF"))
    return tokens


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def consume(self) -> Token:
        tokens = self.tokens[self.pos]
        self.pos += 1
        return tokens

    def expect(self, kind: str) -> Token:
        token = self.consume()
        if token.kind != kind:
            raise SyntaxError(f"Expected {kind}, got {token.kind}")
        return token

    # unary := ('-' | '+') unary | factor
    def parse_unary(self) -> int:
        if self.peek().kind in ("MINUS", "PLUS"):
            op = self.consume().kind
            operand = self.parse_unary()
            return -operand if op == "MINUS" else operand
        return self.parse_factor()

    # factor := NUMBER | '(' expr ')'
    def parse_factor(self) -> int:
        tok = self.peek()
        if tok.kind == "NUM":
            self.consume()
            return tok.value
        if tok.kind == "LPAREN":
            self.consume()
            value = self.parse_expr()  # ← recurse to the top
            self.expect("RPAREN")
            return value
        raise SyntaxError(f"Expected NUM or '(', got {tok.kind}")

    # term := unary (('*' | '/') unary)*
    def parse_term(self) -> int:
        left = self.parse_unary()  # ← was parse_factor
        while self.peek().kind in ("STAR", "SLASH"):
            op = self.consume().kind
            right = self.parse_unary()  # ← was parse_factor
            if op == "STAR":
                left = left * right
            else:
                left = int(left / right) if (left < 0) ^ (right < 0) else left // right
        return left

    # expr := term (('+' | '-') term)*
    def parse_expr(self) -> int:
        left = self.parse_term()
        while self.peek().kind in ("PLUS", "MINUS"):
            op = self.consume().kind
            right = self.parse_term()
            left = left + right if op == "PLUS" else left - right
        return left


def evaluate(source: str) -> int:
    tokens = tokenize(source)
    parser = Parser(tokens)
    result = parser.parse_expr()
    parser.expect("EOF")  # ensure we consumed everything
    return result


# ---------- Tests ----------


def run_tests() -> None:
    assert evaluate("1 + 2") == 3
    assert evaluate("3 + 4 * 2") == 11
    assert evaluate("10 - 2 - 3") == 5
    assert evaluate("20 / 4 / 5") == 1
    assert evaluate("  7  ") == 7
    assert evaluate("100") == 100
    assert evaluate("2 * 3 + 4 * 5") == 26
    print("Stage 1 tests passed.")

    # Parens
    assert evaluate("(1 + 2) * 3") == 9
    assert evaluate("((1 + 2)) * 3") == 9
    assert evaluate("2 * (3 + 4)") == 14
    assert evaluate("(1 + (2 * (3 + 4)))") == 15

    # Unary minus
    assert evaluate("-5") == -5
    assert evaluate("-5 + 3") == -2
    assert evaluate("3 + -5") == -2
    assert evaluate("3 * -4") == -12
    assert evaluate("-3 * -4") == 12
    assert evaluate("--5") == 5
    assert evaluate("---5") == -5
    assert evaluate("-(2 + 3)") == -5
    assert evaluate("+5") == 5

    # Errors (optional)
    try:
        evaluate("(1 + 2")
        assert False, "expected error"
    except SyntaxError:
        pass

    print("Stage 2 tests passed.")


if __name__ == "__main__":
    run_tests()

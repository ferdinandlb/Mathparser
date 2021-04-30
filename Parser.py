from dataclasses import dataclass
from enum import Enum

STRNUMBERS = "0123456789"

class Operator:
    plus = "+"
    minus = "-"
    mul = "*"
    div = "/"
    lparen = "("
    rparen = ")"

@dataclass
class Number:
    value: float

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

@dataclass
class ExpressionNode:
    lnumber: Number
    rnumber: Number
    operator: Operator

    def __repr__(self):
        return str(self.lnumber.value) + self.operator + str(self.rnumber.value)

class Parser:
    def __init__(self, expression):
        self.expression = expression
        self.iterator = iter(self.expression)

    def tokanize(self):
        tokens = []
        self.current = self.advance()
        while self.current:
            if self.current in STRNUMBERS + ".":
                tokens.append(self.make_number())
                continue
            elif self.current == "+":
                tokens.append(Operator.plus)
            elif self.current == "-":
                tokens.append(Operator.minus)
            elif self.current == "*":
                tokens.append(Operator.mul)
            elif self.current == "/":
                tokens.append(Operator.div)
            elif self.current == "(":
                tokens.append(Operator.lparen)
            elif self.current == ")":
                tokens.append(Operator.rparen)
            else:
                raise Exception("ParseError: Invalid token")
            self.current = self.advance()
        return tokens

    def make_number(self):
        strnum = self.current
        self.current = self.advance()
        while self.current and self.current in STRNUMBERS + ".":
            strnum += self.current
            self.current = self.advance()
        return Number(float(strnum))

    def advance(self):
        try:
            return next(self.iterator)
        except StopIteration:
            return None


class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0

    def eval(self):
        self.eval_parens()
        self.idx = 0
        self.eval_factors()
        self.idx = 0
        self.eval_rest()
        return self.tokens

    def eval_parens(self):
        while self.idx < len(self.tokens):
            if self.tokens[self.idx] == Operator.lparen:
                term_tokens = self.make_term()
                self.tokens.insert(self.idx, Interpreter(term_tokens).eval()[0])
            self.idx += 1

    def eval_factors(self):
        while self.idx < len(self.tokens):
            if self.tokens[self.idx] == Operator.mul or self.tokens[self.idx] == Operator.div:
                expr = self.make_expr()

                if expr.operator == Operator.mul:
                    self.tokens.insert(self.idx, Number(expr.lnumber.value * expr.rnumber.value))
                else:
                    self.tokens.insert(self.idx, Number(expr.lnumber.value / expr.rnumber.value))
            self.idx += 1

    def eval_rest(self):
        while self.idx < len(self.tokens):
            if self.tokens[self.idx] == Operator.plus or self.tokens[self.idx] == Operator.plus:
                expr = self.make_expr()

                if expr.operator == Operator.plus:
                    self.tokens.insert(self.idx, Number(expr.lnumber.value + expr.rnumber.value))
                else:
                    self.tokens.insert(self.idx, Number(expr.lnumber.value - expr.rnumber.value))
            self.idx += 1

    def make_expr(self):
        self.idx -= 1
        lnum = self.tokens.pop(self.idx)
        op = self.tokens.pop(self.idx)
        rnum = self.tokens.pop(self.idx)
        return ExpressionNode(lnum, rnum, op)

    def make_term(self):
        term = []
        self.tokens.pop(self.idx)
        while self.tokens[self.idx] != Operator.rparen:
            term.append(self.tokens.pop(self.idx))
        self.tokens.pop(self.idx)
        return term

if __name__ == "__main__":
    while True:
        expr = input(">> ")
        p = Parser(expr)
        tokens = p.tokanize()

        i = Interpreter(tokens)
        print(i.eval()[0].value)
from dataclasses import dataclass
from typing import List, Protocol


class Expression: pass
class Statement: pass


@dataclass
class Program:
    statements: List[Statement]


@dataclass
class LetStatement(Statement):
    name: str
    value: Expression
    line: int


@dataclass
class AssignStatement(Statement):
    name: str
    value: Expression
    line: int


@dataclass
class PrintStatement(Statement):
    value: Expression
    line: int


@dataclass
class BinaryOp(Expression):
    op: str
    left: Expression
    right: Expression
    line: int


@dataclass
class UnaryOp(Expression):
    op: str
    operand: Expression
    line: int


@dataclass
class IntLiteral(Expression):
    value: int
    line: int


@dataclass
class FloatLiteral(Expression):
    value: float
    line: int


@dataclass
class Identifier(Expression):
    name: str
    line: int


class ASTPrinter:
    def print(self, node):
        return self._visit(node)

    def _visit(self, node):
        if isinstance(node, Program):
            return "Program(" + ", ".join(self._visit(s) for s in node.statements) + ")"
        if isinstance(node, LetStatement):
            return f"Let({node.name}, {self._visit(node.value)})"
        if isinstance(node, AssignStatement):
            return f"Assign({node.name}, {self._visit(node.value)})"
        if isinstance(node, PrintStatement):
            return f"Print({self._visit(node.value)})"
        if isinstance(node, BinaryOp):
            return f"({node.op} {self._visit(node.left)} {self._visit(node.right)})"
        if isinstance(node, UnaryOp):
            return f"({node.op} {self._visit(node.operand)})"
        if isinstance(node, IntLiteral):
            return str(node.value)
        if isinstance(node, FloatLiteral):
            return str(node.value)
        if isinstance(node, Identifier):
            return node.name
        return repr(node)

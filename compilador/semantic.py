from .ast_nodes import *
from .errors import SemanticError


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, type_, line):
        if name in self.symbols:
            raise SemanticError(f"variável '{name}' já declarada", line)
        self.symbols[name] = type_

    def lookup(self, name, line):
        if name not in self.symbols:
            raise SemanticError(f"variável '{name}' usada sem declaração", line)
        return self.symbols[name]


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()

    def analyze(self, program: Program):
        for stmt in program.statements:
            self._stmt(stmt)
        return self.symbols

    def _stmt(self, stmt):
        if isinstance(stmt, LetStatement):
            t = self._expr(stmt.value)
            self.symbols.define(stmt.name, t, stmt.line)
        elif isinstance(stmt, AssignStatement):
            if stmt.name not in self.symbols.symbols:
                raise SemanticError(f"use 'let {stmt.name} = ...' para declarar", stmt.line)
            self._expr(stmt.value)
        elif isinstance(stmt, PrintStatement):
            self._expr(stmt.value)

    def _expr(self, expr):
        if isinstance(expr, IntLiteral): return 'int'
        if isinstance(expr, FloatLiteral): return 'float'
        if isinstance(expr, Identifier): return self.symbols.lookup(expr.name, expr.line)
        if isinstance(expr, UnaryOp): return self._expr(expr.operand)
        if isinstance(expr, BinaryOp):
            left = self._expr(expr.left); right = self._expr(expr.right)
            if expr.op == '/': return 'float'
            return 'float' if 'float' in (left, right) else 'int'
        raise SemanticError('expressão inválida')

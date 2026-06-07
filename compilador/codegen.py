from .ast_nodes import *
from .errors import VMRuntimeError


class CodeGenerator:
    def generate(self, program: Program):
        self.instructions = []
        for stmt in program.statements:
            self._stmt(stmt)
        self.instructions.append(('HALT',))
        return self.instructions

    def _stmt(self, stmt):
        if isinstance(stmt, LetStatement):
            self._expr(stmt.value); self.instructions.append(('STORE', stmt.name))
        elif isinstance(stmt, AssignStatement):
            self._expr(stmt.value); self.instructions.append(('STORE', stmt.name))
        elif isinstance(stmt, PrintStatement):
            self._expr(stmt.value); self.instructions.append(('PRINT', stmt.line))

    def _expr(self, expr):
        if isinstance(expr, IntLiteral): self.instructions.append(('PUSH', expr.value, expr.line))
        elif isinstance(expr, FloatLiteral): self.instructions.append(('PUSH', expr.value, expr.line))
        elif isinstance(expr, Identifier): self.instructions.append(('LOAD', expr.name, expr.line))
        elif isinstance(expr, UnaryOp):
            self._expr(expr.operand); self.instructions.append(('NEG', expr.line))
        elif isinstance(expr, BinaryOp):
            self._expr(expr.left); self._expr(expr.right)
            ops = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}
            self.instructions.append((ops[expr.op], expr.line))


class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.env = {}
        self.output = []

    def run(self, instructions):
        ip = 0
        while ip < len(instructions):
            instr = instructions[ip]
            op, *args = instr
            if op == 'PUSH':
                self.stack.append(args[0])
            elif op == 'LOAD':
                name, line = args
                self.stack.append(self.env[name])
            elif op == 'STORE':
                self.env[args[0]] = self.stack.pop()
            elif op == 'ADD':
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a + b)
            elif op == 'SUB':
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a - b)
            elif op == 'MUL':
                b = self.stack.pop(); a = self.stack.pop(); self.stack.append(a * b)
            elif op == 'DIV':
                line = args[0]
                b = self.stack.pop(); a = self.stack.pop()
                if b == 0:
                    raise VMRuntimeError('divisão por zero', line)
                self.stack.append(a / b)
            elif op == 'NEG':
                self.stack.append(-self.stack.pop())
            elif op == 'PRINT':
                self.output.append(str(self.stack.pop()))
            elif op == 'HALT':
                break
            else:
                raise VMRuntimeError(f'instrução desconhecida {op}')
            ip += 1
        return self.output

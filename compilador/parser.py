from typing import List
from .lexer import Token, TokenType
from .errors import ParseError
from .ast_nodes import *


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements = []
        self._skip_separators()
        while not self._check(TokenType.EOF):
            statements.append(self._statement())
            if not self._check(TokenType.EOF):
                self._consume_separator()
            self._skip_separators()
        return Program(statements)

    def _statement(self):
        if self._match(TokenType.LET):
            return self._let_stmt()
        if self._match(TokenType.PRINT):
            return self._print_stmt()
        if self._check(TokenType.IDENTIFIER):
            return self._assign_stmt()
        tok = self._peek()
        raise ParseError(f"'{tok.value}' inesperado neste contexto", tok.line, tok.col)

    def _let_stmt(self):
        let_tok = self._previous()
        name = self._consume(TokenType.IDENTIFIER, "identificador esperado após 'let'")
        self._consume(TokenType.ASSIGN, "'=' esperado após identificador")
        return LetStatement(name.value, self._expression(), let_tok.line)

    def _assign_stmt(self):
        name = self._consume(TokenType.IDENTIFIER, "identificador esperado")
        self._consume(TokenType.ASSIGN, "'=' esperado após identificador")
        return AssignStatement(name.value, self._expression(), name.line)

    def _print_stmt(self):
        print_tok = self._previous()
        self._consume(TokenType.LPAREN, "'(' esperado após 'print'")
        value = self._expression()
        self._consume(TokenType.RPAREN, "')' esperado")
        return PrintStatement(value, print_tok.line)

    def _expression(self):
        expr = self._term()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            op = self._previous()
            if self._is_expr_end():
                raise ParseError(f"expressão incompleta após '{op.value}'", op.line, op.col)
            right = self._term()
            expr = BinaryOp(op.value, expr, right, op.line)
        return expr

    def _term(self):
        expr = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            op = self._previous()
            if self._is_expr_end():
                raise ParseError(f"expressão incompleta após '{op.value}'", op.line, op.col)
            right = self._unary()
            expr = BinaryOp(op.value, expr, right, op.line)
        return expr

    def _unary(self):
        if self._match(TokenType.MINUS):
            op = self._previous()
            if self._is_expr_end():
                raise ParseError("expressão incompleta após '-'", op.line, op.col)
            return UnaryOp('-', self._unary(), op.line)
        return self._primary()

    def _primary(self):
        if self._match(TokenType.INTEGER):
            t = self._previous(); return IntLiteral(t.value, t.line)
        if self._match(TokenType.FLOAT):
            t = self._previous(); return FloatLiteral(t.value, t.line)
        if self._match(TokenType.IDENTIFIER):
            t = self._previous(); return Identifier(t.value, t.line)
        if self._match(TokenType.LPAREN):
            start = self._previous()
            expr = self._expression()
            if not self._match(TokenType.RPAREN):
                found = self._peek()
                found_name = 'EOF' if found.type == TokenType.EOF else repr(found.value)
                raise ParseError(f"')' esperado, encontrado {found_name}", start.line, start.col)
            return expr
        tok = self._peek()
        if tok.type in (TokenType.NEWLINE, TokenType.SEMICOLON, TokenType.EOF, TokenType.RPAREN):
            raise ParseError("expressão incompleta", tok.line, tok.col)
        raise ParseError(f"'{tok.value}' inesperado neste contexto", tok.line, tok.col)

    def _consume_separator(self):
        if self._match(TokenType.NEWLINE, TokenType.SEMICOLON): return
        tok = self._peek()
        raise ParseError("separador esperado", tok.line, tok.col)

    def _skip_separators(self):
        while self._match(TokenType.NEWLINE, TokenType.SEMICOLON): pass

    def _is_expr_end(self):
        return self._check(TokenType.NEWLINE) or self._check(TokenType.SEMICOLON) or self._check(TokenType.EOF) or self._check(TokenType.RPAREN)

    def _match(self, *types):
        if self._check(*types):
            self._advance(); return True
        return False

    def _consume(self, type_, message):
        if self._check(type_): return self._advance()
        tok = self._peek()
        raise ParseError(message, tok.line, tok.col)

    def _check(self, *types):
        return self._peek().type in types

    def _advance(self):
        if not self._check(TokenType.EOF): self.current += 1
        return self._previous()

    def _peek(self): return self.tokens[self.current]
    def _previous(self): return self.tokens[self.current - 1]

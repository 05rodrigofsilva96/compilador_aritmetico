from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List
from .errors import LexerError


class TokenType(Enum):
    INTEGER = auto(); FLOAT = auto(); IDENTIFIER = auto()
    LET = auto(); PRINT = auto()
    PLUS = auto(); MINUS = auto(); STAR = auto(); SLASH = auto()
    ASSIGN = auto(); LPAREN = auto(); RPAREN = auto()
    SEMICOLON = auto(); NEWLINE = auto(); EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: Any
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.col})"


KEYWORDS = {"let": TokenType.LET, "print": TokenType.PRINT}


class Lexer:
    def tokenize(self, source: str) -> List[Token]:
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []
        while not self._is_at_end():
            ch = self._peek()
            if ch in ' \t\r':
                self._advance()
            elif ch == '#':
                self._skip_comment()
            elif ch == '\n':
                self._add(TokenType.NEWLINE, '\n')
                self._advance()
            elif ch.isdigit():
                self._read_number()
            elif ch.isalpha() or ch == '_':
                self._read_identifier()
            else:
                self._single_char(ch)
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return self.tokens

    def _is_at_end(self):
        return self.pos >= len(self.source)

    def _peek(self):
        return '\0' if self._is_at_end() else self.source[self.pos]

    def _peek_next(self):
        return '\0' if self.pos + 1 >= len(self.source) else self.source[self.pos + 1]

    def _advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _add(self, type_, value=None, line=None, col=None):
        self.tokens.append(Token(type_, value, line or self.line, col or self.col))

    def _skip_comment(self):
        while not self._is_at_end() and self._peek() != '\n':
            self._advance()

    def _read_number(self):
        start_pos, start_col, start_line = self.pos, self.col, self.line
        while self._peek().isdigit():
            self._advance()
        is_float = False
        if self._peek() == '.' and self._peek_next().isdigit():
            is_float = True
            self._advance()
            while self._peek().isdigit():
                self._advance()
        text = self.source[start_pos:self.pos]
        if is_float:
            self._add(TokenType.FLOAT, float(text), start_line, start_col)
        else:
            self._add(TokenType.INTEGER, int(text), start_line, start_col)

    def _read_identifier(self):
        start_pos, start_col, start_line = self.pos, self.col, self.line
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()
        text = self.source[start_pos:self.pos]
        self._add(KEYWORDS.get(text, TokenType.IDENTIFIER), text, start_line, start_col)

    def _single_char(self, ch):
        mapping = {
            '+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.STAR,
            '/': TokenType.SLASH, '=': TokenType.ASSIGN, '(': TokenType.LPAREN,
            ')': TokenType.RPAREN, ';': TokenType.SEMICOLON,
        }
        if ch in mapping:
            self._add(mapping[ch], ch)
            self._advance()
        else:
            raise LexerError(f"caractere '{ch}' não reconhecido", self.line, self.col)

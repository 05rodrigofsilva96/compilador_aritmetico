class CompilerError(Exception):
    """Erro base do compilador."""
    def __init__(self, message, line=None, col=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col


class LexerError(CompilerError):
    def __str__(self):
        if self.line is not None and self.col is not None:
            return f"Erro Léxico (L{self.line}:C{self.col}): {self.message}"
        return f"Erro Léxico: {self.message}"


class ParseError(CompilerError):
    def __str__(self):
        if self.line is not None:
            return f"Erro Sintático (L{self.line}): {self.message}"
        return f"Erro Sintático: {self.message}"


class SemanticError(CompilerError):
    def __str__(self):
        if self.line is not None:
            return f"Erro Semântico (L{self.line}): {self.message}"
        return f"Erro Semântico: {self.message}"


class VMRuntimeError(CompilerError):
    def __str__(self):
        if self.line is not None:
            return f"Erro de Execução: {self.message} na linha {self.line}"
        return f"Erro de Execução: {self.message}"

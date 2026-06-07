import pytest
from compilador import run_source, compile_source
from compilador.errors import LexerError, ParseError, SemanticError, VMRuntimeError


def run(code):
    return run_source(code)


def test_add(): assert run('print(2 + 3)') == ['5']
def test_sub(): assert run('print(10 - 4)') == ['6']
def test_mul(): assert run('print(6 * 7)') == ['42']
def test_div(): assert run('print(10 / 4)') == ['2.5']
def test_precedence(): assert run('print(2 + 3 * 4)') == ['14']
def test_parentheses(): assert run('print((2 + 3) * 4)') == ['20']
def test_unary(): assert run('print(-5 + 2)') == ['-3']
def test_float_sum(): assert run('print(1.5 + 2)') == ['3.5']
def test_variable_let(): assert run('let x = 9\nprint(x)') == ['9']
def test_assignment(): assert run('let x = 1\nx = x + 4\nprint(x)') == ['5']
def test_many_prints(): assert run('print(1)\nprint(2)') == ['1', '2']
def test_comments(): assert run('# oi\nlet x = 3 # teste\nprint(x)') == ['3']
def test_semicolon(): assert run('let x = 3; print(x + 1)') == ['4']
def test_area(): assert run('let base = 7.5\nlet altura = 4.0\nlet area = (base * altura) / 2\nprint(area)') == ['15.0']
def test_bytecode_has_halt(): assert compile_source('print(1)')[-1] == ('HALT',)

def test_lexer_error():
    with pytest.raises(LexerError): run('print(@)')

def test_var_not_declared():
    with pytest.raises(SemanticError): run('print(y)')

def test_redeclaration():
    with pytest.raises(SemanticError): run('let x = 1\nlet x = 2')

def test_assignment_without_declaration():
    with pytest.raises(SemanticError): run('z = 3')

def test_division_by_zero():
    with pytest.raises(VMRuntimeError): run('print(10 / 0)')

def test_missing_rparen():
    with pytest.raises(ParseError): run('print((2 + 3)')

def test_incomplete_expression():
    with pytest.raises(ParseError): run('print(2 +)')

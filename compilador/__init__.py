from .lexer import Lexer
from .parser import Parser
from .semantic import SemanticAnalyzer
from .codegen import CodeGenerator, VirtualMachine


def compile_source(source):
    tokens = Lexer().tokenize(source)
    ast = Parser(tokens).parse()
    SemanticAnalyzer().analyze(ast)
    instructions = CodeGenerator().generate(ast)
    return instructions


def run_source(source):
    instructions = compile_source(source)
    vm = VirtualMachine()
    vm.run(instructions)
    return vm.output
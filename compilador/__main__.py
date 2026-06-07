import argparse
import sys
from . import Lexer, Parser, SemanticAnalyzer, CodeGenerator, VirtualMachine
from .ast_nodes import ASTPrinter
from .errors import CompilerError


def main(argv=None):
    argp = argparse.ArgumentParser(prog='python -m compilador')
    argp.add_argument('file', nargs='?', help='arquivo .al')
    argp.add_argument('-c', '--code', help='código inline')
    argp.add_argument('-v', '--verbose', action='store_true', help='mostra tokens, AST e bytecode')
    args = argp.parse_args(argv)

    if args.code is not None:
        source = args.code
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            source = f.read()
    else:
        argp.error('informe um arquivo ou use -c')

    try:
        tokens = Lexer().tokenize(source)
        ast = Parser(tokens).parse()
        SemanticAnalyzer().analyze(ast)
        bytecode = CodeGenerator().generate(ast)
        if args.verbose:
            print('TOKENS:')
            for t in tokens: print(' ', t)
            print('AST:')
            print(' ', ASTPrinter().print(ast))
            print('BYTECODE:')
            for i in bytecode: print(' ', i)
            print('SAÍDA:')
        vm = VirtualMachine()
        for line in vm.run(bytecode):
            print(line)
    except CompilerError as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

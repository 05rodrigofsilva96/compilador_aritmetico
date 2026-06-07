# Compilador ArithLang

Projeto desenvolvido para a disciplina de Teoria da Computação e Compiladores do curso de Engenharia da Computação.

## Objetivo

Implementar, do zero, um compilador funcional para a linguagem ArithLang, contemplando as seguintes fases:

* Análise Léxica (Lexer)
* Análise Sintática (Parser)
* Construção da AST
* Análise Semântica
* Geração de Bytecode
* Execução em Máquina Virtual (VM)

A linguagem suporta:

* Declaração de variáveis (`let`)
* Atribuição
* Inteiros e números reais
* Operações aritméticas (`+`, `-`, `*`, `/`)
* Parênteses
* Comentários (`#`)
* Comando `print`

---

## Estrutura do Projeto

```text
compilador_aritmetico/
│
├── compilador/
│   ├── lexer.py
│   ├── parser.py
│   ├── ast_nodes.py
│   ├── semantic.py
│   ├── codegen.py
│   ├── __init__.py
│   └── __main__.py
│
├── tests/
│   └── test_compiler.py
│
├── examples/
│   ├── exemplo1.al
│   ├── exemplo2.al
│   └── exemplo3.al
│
├── README.md
└── pyproject.toml
```

---

## Instalação

```bash
pip install -e .
```

---

## Execução

Executar um arquivo:

```bash
python -m compilador examples/exemplo1.al
```

Executar código inline:

```bash
python -m compilador -c "let x = 10 * 2\nprint(x)"
```

Modo verbose (tokens, AST e bytecode):

```bash
python -m compilador -v examples/exemplo2.al
```

---

## Testes

Executar todos os testes automatizados:

```bash
python -m pytest
```

O projeto possui mais de 20 casos de teste cobrindo:

* Operações aritméticas
* Precedência de operadores
* Parênteses
* Variáveis
* Comando print
* Erros léxicos
* Erros sintáticos
* Erros semânticos
* Divisão por zero
* Geração de bytecode

---

## Pipeline de Compilação

```text
Fonte
  ↓
Lexer
  ↓
Parser
  ↓
AST
  ↓
Análise Semântica
  ↓
Geração de Bytecode
  ↓
Máquina Virtual (VM)
```

---

### Uso de Inteligência Artificial

Durante o desenvolvimento deste projeto foi utilizado o ChatGPT para algumas funcionalidades nas seguintes etapas:

* Estruturação inicial do analisador léxico (Lexer) e definição dos tokens da linguagem.
* Esclarecimento de dúvidas sobre a implementação do parser de descida recursiva e construção da AST.
* Sugestões para a implementação da análise semântica e da tabela de símbolos.
* Apoio na geração de bytecode e na implementação da máquina virtual baseada em pilha.
* Auxílio na elaboração e revisão dos testes automatizados.
* Suporte na identificação e correção de erros encontrados durante o desenvolvimento.


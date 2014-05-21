AST Calculator
==============

Simple calculator based on [Abstract syntax tree](http://en.wikipedia.org/wiki/Abstract_syntax_tree).
In this case Python's [AST](https://docs.python.org/2/library/ast.html).

Usage
=====

Interactive mode:

    ./calc.py

One off evaluation from command line:

    ./calc.py "1 + 2"

Evaluation of all expression in the file:

    ./calc.py -f input_file

Help, as always:

    ./calc.py --help

Tests
=====

To run test execute:

    python -m unittest discover

Functionality
=============

Allowed
-------
- All operators defined in ast
- Functions: log, exp, sqrt, sin, cos
- Const: pi, e

Not allowed
-----------
- All other things ;) That included executing Python code

#!/usr/bin/env python
"""
Caclulator based on AST
"""

import ast
import math
import operator
import sys

from optparse import OptionParser


def evaluate(node):
    """
    Walk recursively though the mathematical expression,
    in order to evaluate it.

    Valid operations are listed in op_map.
    Valid functions are listed in func_map.
    Valid constants are listed in const_map.
    """

    op_map = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitAnd: operator.and_,
        ast.BitXor: operator.xor,
    }

    func_map = {
        "log": math.log,
        "exp": math.exp,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
    }

    const_map = {
        "pi": math.pi,
        "e": math.e,
    }

    if isinstance(node, (list, tuple)):
        return [evaluate(sub_node) for sub_node in node]

    elif isinstance(node, str):
        return evaluate(ast.parse(node))

    elif isinstance(node, ast.Module):
        values = []
        for body in node.body:
            values.append(evaluate(body))
        if len(values) == 1:
            values = values[0]
        return values

    elif isinstance(node, ast.Expr):
        return evaluate(node.value)

    elif isinstance(node, ast.BinOp):
        left = evaluate(node.left)
        op = node.op
        right = evaluate(node.right)

        try:
            return op_map[type(op)](left, right)
        except KeyError:
            raise ValueError(
                "Operator %s not supported" % op.__class__.__name__)

    elif isinstance(node, ast.Call):
        func_name = node.func.id
        args = [evaluate(arg) for arg in node.args]

        try:
            return func_map[func_name](*args)
        except KeyError:
            raise ValueError("Function %s not supported" % func_name)

    elif isinstance(node, ast.Num):
        return node.n

    elif isinstance(node, ast.Name):
        try:
            return const_map[node.id]
        except KeyError:
            raise ValueError("Constant %s not supported" % node.id)

    raise TypeError("Unsupported operation: %s" % node.__class__.__name__)


def interactive():
    """
    Evaluates expressions given by user in interactive fashion
    """

    print "Please specify expressions to evaluate"
    print "To exit please enter: empty line or word 'quit'"
    print ""

    while True:
        expression = raw_input(">>> ")
        if expression in ["", "quit"]:
            print "Bye"
            break

        try:
            print evaluate(expression)
        except StandardError, err:
            print "Your expression could not be evaluated:", err


def from_file(filename):
    """
    Runs expressions found in given file
    """

    input_file = file(filename, "r")

    for line in input_file:
        expression = line.strip()
        try:
            print "%s = %s" % (expression, evaluate(expression))
        except StandardError, err:
            print "%s could not be evaluated: %s" % (expression, err)


def main(argv):
    description = "Program evaluates mathematical expressions."
    epilog = "By default user will be prompted to input expression."
    usage = "usage: %prog [expression | options]"
    parser = OptionParser(description=description,
                          epilog=epilog,
                          usage=usage)

    parser.add_option("-f", "--file", dest="filename",
                      help="Load expressions from file")

    (options, args) = parser.parse_args(argv)

    if len(args) == 2:
        # Evaluate expression from argument
        try:
            print evaluate(args[1])
        except StandardError, err:
            print "Your expression could not be evaluated:", err
            sys.exit(1)

    elif options.filename:
        # Evaluate expressions in batch mode
        try:
            from_file(options.filename)
        except IOError, err:
            print "There was a problem with your file:", err
            sys.exit(1)

    else:
        # Evaluate expressions entered by user
        interactive()

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)

"""
Test cases for AST calculator
"""

from unittest import TestCase
from calc import evaluate


class TestCaclEvaluate(TestCase):
    """
    Test cases for AST calculator - evaluation
    """

    def test_simple_expression(self):
        """
        Test expression without functions or constants
        """

        data = [
            ("84-9*3", 57),
            ("8**4", 4096),
            ("3*(2*5)**3/(123-32+9)", 30),
        ]

        for expression, expected in data:
            result = evaluate(expression)

            msg = "{} evaluated to: {}. Expected {}".format(
                expression, result, expected)
            self.assertEquals(result, expected, msg)

    def test_complex_expression(self):
        """
        Test expression with functions or constants
        """

        data = [
            ("2*log(exp(2))", 4),
            ("cos(2*pi)", 1),
            ("log(8,2)", 3),
        ]

        for expression, expected in data:
            result = evaluate(expression)

            msg = "{} evaluated to: {}. Expected {}".format(
                expression, result, expected)
            self.assertEquals(result, expected, msg)

    def test_invalid_expression(self):
        """
        Make sure code will behave correctly for invalid input
        """

        data = [
            "1/0",
            "import os",
        ]

        for expression in data:
            with self.assertRaises(StandardError):
                evaluate(expression)

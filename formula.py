"""
Copyright© 2024 Artur Pozniak <noi.kucia@gmail.com> or <noiszewczyk@gmail.com>.
All rights reserved.
This program is released under license GPL-3.0-or-later

This file is part of MathGraph.
MathGraph is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

MathGraph is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with MathGraph.
If not, see <https://www.gnu.org/licenses/>.
"""

import math
import random
import re

operators_precedence = {'-': 1, '+': 1, '*': 4, '/': 4, '%': 4, '^': 5, '(': 10, ')': 10}
constants = {'pi': 3.141592_653589_793238, 'e': 2.718281828459045}
functions = {'abs': abs, 'sqrt': math.sqrt, 'rt': math.sqrt, 'exp': math.exp, 'tan': math.tan, 'tg': math.tan,
             'sin': math.sin, 'cos': math.cos, 'log': math.log10, 'lg': math.log10, 'ln': lambda x: math.log(math.e, x)}
functions_precedence = 2
maximum_value = 50000


class TranslateError(Exception):
    pass


class NumberError(TranslateError):
    pass


class ParenthesesError(TranslateError):
    pass


class TokenError(TranslateError):
    pass


class EvaluatingError:
    pass


class DividingZero(EvaluatingError):
    pass


class ArgumentOutOfRange(EvaluatingError):
    pass


class Formula:
    formula = []

    def __init__(self, infix_formula: str):
        self.formula = self.translate_to_postfix(infix_formula)

    def translate_to_postfix(self, infix_formula: str):
        if not infix_formula:
            raise TranslateError  # if infix_formula is empty

        # preparing string to translate
        infix_formula = infix_formula.replace('\n', '')
        infix_formula = infix_formula.lower()
        if infix_formula[0] == '-':
            infix_formula = '0' + infix_formula
        infix_formula = re.sub(r'\(\s*-', '(0-', infix_formula)  # adding 0 before unary '-'
        infix_formula = re.sub(r'(\d)\s*([a-zA-Z(])', r'\1*\2', infix_formula)  # adding '*' signs
        infix_formula = re.sub(r'\)\(', ')*(', infix_formula)
        infix_formula = re.sub(r':', '/', infix_formula)  # changing ':' to '/'

        postfix_formula = []
        operators_stack = []
        i = -1
        while i + 1 < len(infix_formula):  # while infix_formula has more than 1 element
            i += 1

            symbol_to_parse = infix_formula[i]

            if symbol_to_parse in (' ', '\t', '\a', '\r', '\v'):  # skipping whitespaces
                continue

            if symbol_to_parse.isdigit():  # numbers
                num = symbol_to_parse
                while (i + 1 < len(infix_formula)) and (infix_formula[i + 1].isdigit() or infix_formula[i + 1] == '.'):
                    i += 1
                    num += infix_formula[i]
                # adding number to the output
                try:
                    postfix_formula.append(float(num) if '.' in num else int(num))
                except Exception:
                    raise NumberError  # if number is wrong (more than 1 point for example)

            elif symbol_to_parse in operators_precedence.keys():  # operators

                if symbol_to_parse == '(':
                    operators_stack.append('(')

                elif symbol_to_parse == ')':
                    try:
                        # pop all operators from stack until '(' is popped operator and  put them to the output
                        top_el = operators_stack.pop()
                        while not top_el == '(':
                            postfix_formula.append(top_el)
                            top_el = operators_stack.pop()

                        # if before '(' was a function, pop it from stack to the output
                        if len(operators_stack) and (operators_stack[-1] in functions):
                            postfix_formula.append(operators_stack.pop())
                    except Exception:
                        raise ParenthesesError

                else:
                    current_operator_precedence = operators_precedence[symbol_to_parse]

                    # if operator(func) on the top of stack has higher precedence, and it is not '('
                    # then pop it into output before push current operator on stack
                    while len(operators_stack) and (not operators_stack[-1] == '('):
                        token = operators_stack[-1]  # token on the top of stack
                        if token in functions.keys():  # if function on the top of stack
                            if current_operator_precedence < functions_precedence:
                                postfix_formula.append(operators_stack.pop())
                                continue
                            break
                        elif operators_precedence[
                            token] >= current_operator_precedence:  # if operator on the top of stack
                            postfix_formula.append(operators_stack.pop())
                        else:
                            break
                    operators_stack.append(symbol_to_parse)

            elif symbol_to_parse.isalpha():  # constants and functions
                token_end_index = i

                while token_end_index < len(infix_formula) and infix_formula[token_end_index].isalpha():
                    token_end_index += 1

                token = infix_formula[i:token_end_index]  # getting whole token to analyze
                i = token_end_index - 1  # skipping all token

                if token == 'x':
                    postfix_formula.append('x')
                elif token in constants.keys():
                    postfix_formula.append(constants[token])
                elif token in functions.keys():
                    operators_stack.append(token)
                else:
                    raise TokenError

            else:
                raise TokenError  # unknown token

        # popping all operators from stack
        if '(' not in operators_stack:
            if operators_stack:
                while operators_stack:
                    postfix_formula.append(operators_stack.pop())
        else:
            raise ParenthesesError

        # checking if amount of operands and operators_precedence is appropriate
        try:
            postfix_formula_copy = postfix_formula.copy()
            while len(infix_formula) > 1:
                for i in range(len(postfix_formula_copy)):
                    if type(postfix_formula_copy[i]) == str and (not postfix_formula_copy[i] == 'x'):
                        if postfix_formula_copy[i] in operators_precedence.keys():
                            for _ in range(2):
                                postfix_formula_copy.pop(i - 1)
                        else:
                            postfix_formula_copy.pop(i)
                        break
                else:  # if no operators_precedence found
                    if len(postfix_formula_copy) > 1:
                        raise TokenError
                    if type(postfix_formula_copy[0]) == str and not postfix_formula_copy[0] == 'x':
                        raise TokenError
                    break
        except Exception:
            raise TokenError

        return postfix_formula

    def evaluate(self, argument: float = 0) -> float:
        tokens = self.formula.copy()
        try:
            while len(tokens) > 1:
                i = 0
                while 0 <= i < len(tokens):
                    token = tokens[i]
                    if type(token) == str:
                        if token == 'x':
                            tokens[i] = argument
                        elif token in operators_precedence.keys():
                            a, b = tokens[i - 2], tokens[i - 1]
                            match token:
                                case '+':
                                    value = a + b
                                case '-':
                                    value = a - b
                                case '*':
                                    value = a * b
                                case '/':
                                    if b:
                                        value = a / b
                                    else:
                                        raise DividingZero
                                case '^':
                                    try:
                                        if a < 0:
                                            if not (b - int(b)) < 10 / maximum_value:
                                                raise ArgumentOutOfRange
                                            else:
                                                b = int(b)
                                        value = a ** b
                                    except ValueError:
                                        value = maximum_value
                                case '%':
                                    try:
                                        value = a % b
                                    except Exception:
                                        raise ArgumentOutOfRange
                            tokens.pop(i - 1)
                            tokens.pop(i - 1)
                            if value > maximum_value:
                                value = maximum_value + 10 * random.random()  # defending from too big numbers
                            if value < -maximum_value:
                                value = -maximum_value + 10 * random.random()
                            tokens[i - 2] = value
                            i -= 2
                        else:
                            if token == 'exp' and tokens[i - 1] > 100:
                                tokens[i - 1] = 100 + 2 * random.random()
                            tokens[i - 1] = functions[token](tokens[i - 1])
                            tokens.pop(i)
                            i -= 1
                    i += 1
                else:  # no operators_precedence found
                    break
            if len(tokens) == 0:
                raise EvaluatingError
            if tokens[-1] == 'x':
                return argument
            if tokens[-1] > maximum_value:
                return maximum_value
            if tokens[-1] < -maximum_value:
                return -maximum_value
            return float(tokens[-1])
        except Exception:
            raise EvaluatingError


from lark import Lark
import os

def load_parser():
    grammar_path = os.path.join(os.path.dirname(__file__), 'grammar.lark')

    with open(grammar_path, 'r') as grammar_file:
        grammar = grammar_file.read()
    return Lark(grammar, start='start', parser='lalr')

def parse_filter(expression):
    parser = load_parser()
    return parser.parse(expression)

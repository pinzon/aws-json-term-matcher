from lark import Lark, Transformer, v_args
import os

# Transformer to evaluate the parsed filter
@v_args(inline=True)
class FilterEvaluator(Transformer):
    def __init__(self, data):
        self.data = data

    def paren(self, expr):
        return expr

    def and_op(self, left, right):
        return left and right

    def or_op(self, left, right):
        return left or right

    def comparison(self, entity, comparator, value):
        entity_value = self.resolve_entity(entity)
        return self.compare(entity_value, comparator, value)

    def resolve_entity(self, entity):
        # Extract the entity from the dictionary based on selection rules
        # This would resolve $.attribute or $[index] kind of paths in the dictionary
        keys = []
        if isinstance(entity, str):
            keys = entity.split(".")
        value = self.data
        for key in keys:
            if key.isdigit():
                value = value[int(key)]
            else:
                value = value.get(key, None)
        return value

    def compare(self, entity_value, comparator, value):
        if comparator == "=":
            return entity_value == value
        elif comparator == "!=":
            return entity_value != value
        elif comparator == ">":
            return entity_value > value
        elif comparator == ">=":
            return entity_value >= value
        elif comparator == "<":
            return entity_value < value
        elif comparator == "<=":
            return entity_value <= value
        return False

    def value(self, value):
        # Returns the value as-is (for STRING, NUMBER, etc.)
        return value


def load_parser():
    grammar_path = os.path.join(os.path.dirname(__file__), "grammar.lark")

    with open(grammar_path, "r") as grammar_file:
        grammar = grammar_file.read()
    return Lark(grammar, start="start", parser="lalr")


def parse_filter(expression):
    parser = load_parser()
    return parser.parse(expression)


def match(obj: dict, filter: str):
    tree = parse_filter(filter)
    evaluator = FilterEvaluator(obj)

    return evaluator.transform(tree)

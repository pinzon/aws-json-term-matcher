from lark import Lark, Transformer, v_args, Tree, Token
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
        result = self.compare(entity_value, comparator, value)
        return result

    def resolve_entity(self, entity: Tree):
        # Extract the entity from the dictionary based on selection rules
        # This would resolve $.attribute or $[index] kind of paths in the dictionary
        keys = []
        # in this case the three only is composed of branch with just one branch
        # entity -> selection -> attribute access -> "NAME"

        def _resolve(node):
            if node.data == "attribute_access":
                # Handles attributes like $.attributeName or $["attributeName"]
                child = node.children[0]
                if child.type == "NAME":
                    keys.append(child.value)  # Regular attribute
                elif child.type == "ESCAPED_STRING":
                    keys.append(
                        child.value.strip('"')
                    )  # Attribute accessed like ["attr"]

            elif node.data == "index_access":
                # Handles indices like $[0] or $.attribute[1]
                attr = node.children[0].children[0].value
                keys.append(attr)
                index = node.children[
                    1
                ].value  # The index is the second child in the rule
                keys.append(index)

            elif node.data == "selection":
                # Keep recursing through the selection (attributes or indices)
                for child in node.children:
                    _resolve(child)
            elif node.data == "entity":
                for child in node.children:
                    _resolve(child)

        # Start traversing the entity tree to build the keys
        _resolve(entity)

        value = self.data
        for key in keys:
            if key.isdigit():
                value = value[int(key)]
            else:
                value = value.get(key, None)
        return value

    def compare(self, entity_value, comparator, value):
        comparator_value = comparator.value

        if comparator_value == "=":
            return entity_value == value
        elif comparator_value == "!=":
            return entity_value != value
        elif comparator_value == ">":
            return entity_value > value
        elif comparator_value == ">=":
            return entity_value >= value
        elif comparator_value == "<":
            return entity_value < value
        elif comparator_value == "<=":
            return entity_value <= value
        return False

    def value(self, value: Token):
        # Returns the value as-is (for STRING, NUMBER, etc.)
        if value.type in ["SCIENTIFIC", "NUMBER"]:
            return float(value.value)

        return value.value.strip("\"'")


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

    result = evaluator.transform(tree)
    return result.children[0].children[0]

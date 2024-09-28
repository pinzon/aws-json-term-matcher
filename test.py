import filter
from pprint import pprint

# filter_sample = '{($.detail-type ="ShopUnavailable") && (($.resources[1] = "arn:aws:states:us-east-1:111222333444:execution:OrderProcessorWorkflow:d57d4769-72fd") || ($.resources[0] = "arn:aws:states:us-east-1:111222333444:stateMachine:OrderProcessorWorkflow"))}'
# filter_sample =  '{( $.eventType = "UpdateTrail")}'

filter_sample =  '{( $.eventType = "UpdateTrail") ||  (($.eventType = "UpdateTrail2") && ($.eventType[2] = "uts")) }'
# filter_sample = '{ $.sourceIPAddress[0] != "123.123:arn:asdfa-sdf/asdfsd" }'
tree = filter.parse(filter_sample)

def print_tree(node, level=0):
    # Print the current node's text with indentation based on the level
    print('  ' * level + node.text)

    # Recursively print each child node (element)
    for child in node.elements:
        print_tree(child, level + 1)

print_tree(tree)

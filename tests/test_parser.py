import pytest
from aws_json_term_matcher.parser import parse_filter

test_cases = [
    # simple case
    '{ $.eventType = "UpdateTrail" }',

    # numeric values
    "{ $.bandwidth > 75 }",
    "{ $.latency < 50 }",
    "{ $.refreshRate >= 60 }",
    "{ $.responseTime <= 5 }",
    "{ $.errorCode = 400}",
    "{ $.errorCode != 500 }",
    "{ $.number[0] = 1e-3 }",
    "{ $.number[0] != 1e+3 }",

    # ip
    "{ $.sourceIPAddress != 123.123.* }",

    # array
    '{ $.arrayKey[0] = "value"}',

    # grouped and logic operation
    '{( $.eventType = "UpdateTrail") ||  (($.eventType = "UpdateTrail2") && ($.eventType[2] = "uts")) }',

    # real life sample with arn
    '{($.detail-type ="ShopUnavailable") && (($.resources[1] = "arn:aws:states:us-east-1:111222333444:execution:OrderProcessorWorkflow:d57d4769-72fd") || ($.resources[0] = "arn:aws:states:us-east-1:111222333444:stateMachine:OrderProcessorWorkflow"))}',
    ]

@pytest.mark.parametrize("filter", test_cases)
def test_parse_filter(filter):
    result = parse_filter(filter)
    assert result is not None

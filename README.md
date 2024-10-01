# AWS JSON Term Matcher

`aws_json_term_matcher` is a Python package designed to parse and evaluate filter expressions, such as those found in AWS CloudWatch log filters. This tool uses **Lark** for PEG parsing and supports logical operations like `AND`, `OR`, and parentheses for grouping.

## Features
- Parses logical expressions from JSON filters
- Supports `&&` (AND), `||` (OR), and parentheses for nested expressions
- Extensible to include evaluation and tree reduction (future updates)

## Installation

Clone the repository and install the requirements:

```bash
git clone https://github.com/yourusername/aws_json_term_matcher.git
cd aws_json_term_matcher
pip install -r requirements.txt

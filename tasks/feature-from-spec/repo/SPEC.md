# calc.evaluate(expression: str) -> float

Evaluates an arithmetic expression and returns the result as a float.

- Numbers: integers (`42`) and decimals (`4.5`)
- Binary operators: `+`, `-`, `*`, `/`, with the usual precedence (`*` and `/` before `+` and `-`)
  and left associativity (`8 - 3 - 2` is `3`, `8 / 4 / 2` is `1`)
- Parentheses, nested at any depth
- Unary minus: `-3`, `-(2 + 1)`, `2 * -3`
- Whitespace is ignored
- Division by zero raises `ZeroDivisionError`
- Any invalid expression raises `ValueError`, for example: empty string, unbalanced parentheses,
  unknown character, two numbers in a row (`3 4`), trailing operator (`2 +`)
- `eval`, `exec` and any third-party library are forbidden: write a parser

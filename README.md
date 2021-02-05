# Project description

The package can be installed by `pip install cnf_process`.

This small project parses a boolean expression such as `'A1 | B1 & C1'` into an object containing the equivalent sympy boolean expression in conjunctive normal form. The expression can be simply fly by the `evaluate(variable, Result)` function.

```python
from cnf_process import CNFStatement
boolean_expression = CNFStatement('(A1 & A2) | (~B1 & B2 | (C1 & C2))') 
# The boolean_expression.math_statement will be the sympy boolean expression for (A1 & A2) | (~B1 & B2 | (C1 & C2)), which is:
# (A1 | B2 | C1) & (A1 | B2 | C2) & (A2 | B2 | C1) & (A2 | B2 | C2) & (A1 | C1 | ~B1) & (A1 | C2 | ~B1) & (A2 | C1 | ~B1) & (A2 | C2 | ~B1)

```

`boolean_expression` in the given example can be simplified by `evaluate(variable, Result)` function. For example if we know `A1 = True`. Then we can fill in:

```python
boolean_expression.evaluate('A1', True)
# The result is: boolean_expression.math_statement = (A2 | B2 | C1) & (A2 | B2 | C2) & (A2 | C1 | ~B1) & (A2 | C2 | ~B1)
```

# Variable and expression naming rules

Some variable names and symbols in the expressions will crash the program. So please avoid naming the variables in following ways:

1. Variable cannot be an empty string, `'E', 'I', 'O', 'S', 'N'`.
2. String boolean expression cannot have following symbols and the backlash \`: 
   ```python
    ['`', '-', '=', '[', ']' , ';', "'", ',', '.', '/', '!', '@', '#', '$', '%', '^', '*', ':', '<', '>', '?', '·', '+', '"']
   ```
3. Input string and variable cannot start with a number or '_'.
4. Variable names must at least have one letter.
5. Variable names cannot start with a number.
6. The length of each variable should be no longer than 32 characters.

# Reset the CNFStatement object math_statement value
If you wish to give `boolean_expression` in the example above another value, you can do it via the `translate` function, say you want to change it to `'A1 & ~B1'`:
```python
boolean_expression.translate('A1 & ~B1')
```


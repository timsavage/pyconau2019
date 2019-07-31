import ast
import sys

MY_OBJ = {
    "x": 123,
    "y": 321,
    "foo": True,
}


def verify_expression(st):
    # Check for a comparison
    if not isinstance(st.body, ast.Compare):
        raise RuntimeError(f"Expected comparison got {type(expr)}")

    def _validate(node):
        # Allow constant values
        if isinstance(node, ast.Compare):
            _validate(node.left)
            [_validate(c) for c in node.comparators]
        elif isinstance(node, (ast.Num, ast.Str, ast.Bytes, ast.List, ast.Tuple, ast.NameConstant)):
            pass  # Allow all constants
        elif isinstance(node, ast.Name):
            if node.id not in MY_OBJ:
                raise RuntimeError(f"Unknown variable {node.id}")
        else:
            raise RuntimeError(f"Unsupported node {node!r}")



print(f"Object is: {MY_OBJ}")
while True:
    try:
        expr = input("Enter an expression to evaluate obj: ")
    except KeyboardInterrupt:
        print()
        exit()

    try:
        st = ast.parse(expr, mode="eval")
    except SyntaxError as ex:
        print(f"Invalid expression: {ex}")
        continue
    
    try:
        verify_expression(st)
    except RuntimeError as ex:
        print(str(ex))
        continue

    try:
        print(eval(expr, {}, MY_OBJ))
    except Exception as ex:
        print(repr(ex))


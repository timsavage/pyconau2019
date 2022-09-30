#
# WARNING! 
#
# This was simplified and significantly shortened to allow for presentation during my talk 
# and should never be deployed in production.
#

import ast
import readline

MY_EVENT = {"x": 123, "y": "321", "foo": True}


def verify_expression(st):
    """
    Validate and verify event matching expression.
    """

    def _validate(node):
        # Allow and process compare statements
        if isinstance(node, ast.Compare):
            _validate(node.left)
            # Allow all operations so don't check operators
            [_validate(c) for c in node.comparators]

        # Allow certain literals and constants
        elif isinstance(node, (ast.Num, ast.Str, ast.Bytes, ast.List, ast.Tuple, ast.NameConstant)):
            pass

        # Allow certain calls (len)
        elif isinstance(node, ast.Call):
            # Allow use of len
            if isinstance(node.func, ast.Name):
                if node.func.id not in ("len",):
                    raise NameError(f"{node.func.id!r} not found.")

            # Allow use of startswith, endswith
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr not in ("startswith", "endswith"):
                    raise NameError(f"{node.func.attr!r} not found.")

            else:
                raise SyntaxError(f"Unsupported node {node!r}")

        # Filter the available names to those in an event
        elif isinstance(node, ast.Name):
            if node.id not in MY_EVENT:
                raise NameError(f"{node.id!r} not found")

        else:
            raise SyntaxError(f"Unsupported node {node!r}")

    _validate(st.body)


print(f"Event is: {MY_EVENT}")
while True:
    try:
        expr = input("\nMatching expression: ")
    except (KeyboardInterrupt, EOFError):
        print()
        exit()

    try:
        st = ast.parse(expr, mode="eval")
    except SyntaxError as ex:
        print(f"Invalid expression: {ex}")
        continue

    try:
        verify_expression(st)
    except (SyntaxError, NameError) as ex:
        print(str(ex))
        continue

    try:
        matched = eval(expr, {}, MY_EVENT)
    except Exception as ex:
        print(repr(ex))
    else:
        if matched:
            print("Event matched!")

import ast

MY_EVENT = {
    "x": 123,
    "y": "321",
    "foo": True,
}


def verify_expression(st):
    def _validate(node):

        # Allow and process compare statements
        if isinstance(node, ast.Compare):
            _validate(node.left)
            # Allow all operations so don't check operators
            [_validate(c) for c in node.comparators]

        # Allow certain literals and constants
        elif isinstance(node, (ast.Num, ast.Str, ast.Bytes, ast.List, ast.Tuple, ast.NameConstant)):
            pass
        
        # Filter the available names to those in an event
        elif isinstance(node, ast.Name):
            if node.id not in MY_EVENT:
                raise NameError(f"Unknown variable {node.id}")
        
        else:
            raise RuntimeError(f"Unsupported node {node!r}")
    
    _validate(st.body)


print(f"Event is: {MY_EVENT}")
while True:
    try:
        expr = input("\nMatching expression: ")
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
        matched = eval(expr, {}, MY_EVENT)
    except Exception as ex:
        print(repr(ex))
    else:
        if matched:
            print("Event matched!")


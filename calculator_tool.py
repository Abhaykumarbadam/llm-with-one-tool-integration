def calculate(expression: str) -> float:
    try:
        safe_expr = "".join(char for char in expression if char in "0123456789+-*/. ")
        return eval(safe_expr)
    except Exception as e:
        raise ValueError(f"Error in calculation: {e}")

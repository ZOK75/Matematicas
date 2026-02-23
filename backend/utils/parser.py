import sympy as sp


def parse_function(function_str: str):
    """
    Convierte un string matemático en una función evaluable f(x, y).

    Ej acepta expresiones como:
        x + y
        sin(x) - y
        x*y
        exp(x) - y
        log(x) + y

    Retorna:
        función Python f(x, y)
    """

    if not function_str or not function_str.strip():
        raise ValueError("La función no puede estar vacía")

    try:
        # Definir variables simbólicas permitidas
        x, y = sp.symbols('x y')

        # Funciones matemáticas permitidas
        allowed_functions = {
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "exp": sp.exp,
            "log": sp.log,
            "sqrt": sp.sqrt,
        }

        # Convertir string a expresión simbólica segura
        expr = sp.sympify(function_str, locals=allowed_functions)

        # Verificar que solo use x y y
        variables = expr.free_symbols
        if not variables.issubset({x, y}):
            raise ValueError("Solo se permiten las variables x y y")

        # Convertir a función numérica rápida
        func = sp.lambdify((x, y), expr, modules=["math"])

        # Wrapper para manejar errores numéricos
        def safe_function(x_val, y_val):
            try:
                result = func(x_val, y_val)
                return float(result)
            except Exception as e:
                raise ValueError(f"Error al evaluar la función: {e}")

        return safe_function

    except Exception as e:
        raise ValueError(f"Función inválida: {e}")
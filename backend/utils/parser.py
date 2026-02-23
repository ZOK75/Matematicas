
import sympy as sp

def parse_function(function_str: str, metodo: str="euler"):
    if not function_str or not function_str.strip():
        raise ValueError("La función no puede estar vacía")

    try:
        # Normalizar a minúsculas
        function_str = function_str.lower()

        # Definir variables simbólicas
        x, y = sp.symbols('x y')

        # Funciones matemáticas permitidas
        allowed_functions = {
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "exp": sp.exp,
            "log": sp.log,
            "sqrt": sp.sqrt,
            "ln": sp.log,   # alias
            "pow": sp.Pow,  # alias
        }

        # Convertir string a expresión simbólica segura
        expr = sp.sympify(function_str, locals=allowed_functions)

        # Validación según método
        variables = expr.free_symbols
        if metodo in ["euler", "runge_kutta"]:
            if not variables.issubset({x, y}):
                raise ValueError("Solo se permiten las variables x y y")
            func = sp.lambdify((x, y), expr, modules=["math"])
            def safe_function(x_val, y_val):
                try:
                    return float(func(x_val, y_val))
                except Exception as e:
                    raise ValueError(f"Error al evaluar la función: {e}")
            return safe_function

        elif metodo == "newton":
            if not variables.issubset({x}):
                raise ValueError("Solo se permite la variable x")
            func = sp.lambdify(x, expr, modules=["math"])
            def safe_function(x_val):
                try:
                    return float(func(x_val))
                except Exception as e:
                    raise ValueError(f"Error al evaluar la función: {e}")
            return safe_function

        else:
            raise ValueError("Método desconocido")

    except Exception as e:
        raise ValueError(f"Función inválida: {e}")

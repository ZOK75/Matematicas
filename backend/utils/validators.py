from utils.parser import parse_function


def validate_step_size(h):
    """Valida que el tamaño de paso sea positivo."""
    try:
        h = float(h)
    except ValueError:
        raise ValueError("El tamaño de paso h debe ser numérico")

    if h <= 0:
        raise ValueError("El tamaño de paso h debe ser mayor que 0")

    return h


def validate_iterations(n):
    """Valida que el número de iteraciones sea entero positivo."""
    try:
        n = int(n)
    except ValueError:
        raise ValueError("El número de iteraciones debe ser un entero")

    if n <= 0:
        raise ValueError("El número de iteraciones debe ser mayor que 0")

    return n


def validate_initial_values(x0, y0):
    """Valida que los valores iniciales sean numéricos."""
    try:
        x0 = float(x0)
        y0 = float(y0)
    except ValueError:
        raise ValueError("Los valores iniciales x0 y y0 deben ser numéricos")

    return x0, y0


def validate_function(function_str):
    """
    Valida que la función sea correcta y evaluable.
    Retorna la función ya convertida.
    """
    try:
        func = parse_function(function_str)

        # prueba rápida de evaluación para detectar errores ocultos
        func(1.0, 1.0)

        return func

    except Exception as e:
        raise ValueError(f"Función inválida: {e}")


def validate_all(function_str, x0, y0, h, n):
    """
    Valida todos los parámetros del problema.

    Retorna:
        func, x0, y0, h, n  (ya convertidos y seguros)
    """

    func = validate_function(function_str)
    x0, y0 = validate_initial_values(x0, y0)
    h = validate_step_size(h)
    n = validate_iterations(n)

    return func, x0, y0, h, n
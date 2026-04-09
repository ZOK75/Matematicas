import sympy as sp


def newton_raphson(func_str, x0, tol=1e-7):
    x = sp.symbols('x')

    expr = sp.sympify(func_str.replace('^', '**'))
    derivada = sp.diff(expr, x)

    f = sp.lambdify(x, expr, modules=['math'])
    df = sp.lambdify(x, derivada, modules=['math'])

    x_n = float(x0)
    historial = []

    for i in range(50):
        try:
            val_f = f(x_n)
            val_df = df(x_n)

            error = abs(x_n - historial[-1]['x']) if i > 0 else 0.0

            historial.append({
                'iter': i,
                'x': float(x_n),
                'y': float(val_f),
                'error': float(error)
            })

            if abs(val_f) < tol:
                return x_n, historial

            # Evitar división por cero
            if abs(val_df) < 1e-12:
                break

            x_next = x_n - (val_f / val_df)

            if abs(x_next - x_n) < tol:
                historial.append({
                    'iter': i + 1,
                    'x': float(x_next),
                    'y': float(f(x_next)),
                    'error': float(abs(x_next - x_n))
                })
                return x_next, historial

            x_n = x_next

        except Exception as e:
            print(f"Error en iteración {i}: {e}")
            break

    return x_n, historial
import sympy as sp


def newton_raphson(func, x0, tol=1e-7, max_iter=1000):

    if not callable(func):
        print("Error: 'func' debe ser una función.")
        return None

    x = sp.symbols('x')
    f_sym = func(x)
    f_prime_sym = sp.diff(f_sym, x)

    f_num = sp.lambdify(x, f_sym, 'math')
    f_prime_num = sp.lambdify(x, f_prime_sym, 'math')

    x_n = x0
    historial = [x_n]

    for i in range(max_iter):

        try:
            f_x_n = f_num(x_n)
            f_prime_x_n = f_prime_num(x_n)
        except Exception as e:
            print("Error evaluando la función:", e)
            return None

        # división entre cero (numérica)
        if abs(f_prime_x_n) < 1e-12:
            print("Error: derivada cercana a cero.")
            return None

        x_n1 = x_n - f_x_n / f_prime_x_n
        historial.append(x_n1)

        if abs(x_n1 - x_n) < tol:
            return x_n1, historial

        x_n = x_n1

    print("No convergió.")
    return None, historial
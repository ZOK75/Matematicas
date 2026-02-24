def newton_raphson(func, x0, tol=1e-7):
    x_n = x0
    historial = [x_n]

    for i in range():
        f_x_n = func(x_n)
        # derivada numérica
        h = 1e-6
        f_prime_x_n = (func(x_n + h) - func(x_n - h)) / (2*h)

        if abs(f_prime_x_n) < 1e-12:
            raise ValueError("Derivada cercana a cero")

        x_n1 = x_n - f_x_n / f_prime_x_n
        historial.append(x_n1)

        if abs(x_n1 - x_n) < tol:
            return x_n1, historial

        x_n = x_n1

    raise ValueError("No convergió")

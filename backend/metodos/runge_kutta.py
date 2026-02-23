def runge_kutta(f=None, x0=None, y0=None, h=None, n=None):
    if f is None or x0 is None or y0 is None or h is None or n is None:
        print("Error: faltan parámetros para ejecutar Runge-Kutta")
        return None, None

    # aquí va tu código normal
    x_values = [x0]
    y_values = [y0]

    for i in range(n):
        k1 = h * f(x0, y0)
        k2 = h * f(x0 + h/2, y0 + k1/2)
        k3 = h * f(x0 + h/2, y0 + k2/2)
        k4 = h * f(x0 + h, y0 + k3)

        y0 = y0 + (k1 + 2*k2 + 2*k3 + k4) / 6
        x0 = x0 + h

        x_values.append(x0)
        y_values.append(y0)

    return x_values, y_values
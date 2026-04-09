def runge_kutta(f, x0, y0, h, n):
    x_vals = [x0]
    y_vals = [y0]
    ks_historial = [] # Para guardar los valores de k

    x = x0
    y = y0

    for i in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h/2, y + k1/2)
        k3 = h * f(x + h/2, y + k2/2)
        k4 = h * f(x + h, y + k3)

        ks_historial.append({
            'k1': float(k1),
            'k2': float(k2),
            'k3': float(k3),
            'k4': float(k4)
        })

        y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
        x = x + h

        x_vals.append(float(x))
        y_vals.append(float(y))

    return x_vals, y_vals, ks_historial
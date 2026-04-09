def euler_mejorado(f, x0, y0, h, n):
    x_vals = [float(x0)]
    y_vals = [float(y0)]
    detalles = [{'y_pred': 0, 'error': 0}]

    x = x0
    y = y0

    for i in range(n):
        y_pred = y + h * f(x, y)

        y_corr = y + (h / 2) * (f(x, y) + f(x + h, y_pred))

        error = abs(y_corr - y_pred)

        y = y_corr
        x = x + h

        x_vals.append(float(x))
        y_vals.append(float(y))
        detalles.append({
            'y_pred': float(y_pred),
            'error': float(error)
        })

    return x_vals, y_vals, detalles
def euler_mejorado(funcion, x0=None, y0=None, h=None, n=None):
    """
    Método de Euler mejorado para resolver ecuaciones diferenciales ordinarias.
    
    Parametros:
    funcion: función que representa la ecuación diferencial (dy/dx = f(x, y))
    x0: valor inicial de x
    y0: valor inicial de y
    h: tamaño del paso
    n: número de iteraciones
    
    Returns:
    Listas de valores de x e y calculados.
    """
    # Comprobar parámetros faltantes
    missing = []
    if funcion is None:
        missing.append("funcion")
    if x0 is None:
        missing.append("x0")
    if y0 is None:
        missing.append("y0")
    if h is None:
        missing.append("h")
    if n is None:
        missing.append("n")

    if missing:
        print(f"Faltan valores en Euler mejorado: {', '.join(missing)}")
        return None, None

    x_values = [x0]
    y_values = [y0]
    
    for i in range(n):
        x_current = x_values[-1]
        y_current = y_values[-1]
        
        # Calcular el valor intermedio 
        k1 = funcion(x_current, y_current)
        k2 = funcion(x_current + h, y_current + h * k1)
        
        # Actualizar los valores de x e y u
        x_next = x_current + h
        y_next = y_current + (h / 2) * (k1 + k2)
        
        x_values.append(x_next)
        y_values.append(y_next)
    
    return x_values, y_values
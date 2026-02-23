#Este es un archivo temporal para probar los métodos de newton_raphson, Euler y Runge-Kutta. 
# No es un test unitario formal, sino una prueba rápida para verificar que los 
# métodos funcionan con una función simple.


import sympy as sp
from metodos.newton_raphson import newton_raphson
from metodos.euler import euler_mejorado
from metodos.runge_kutta import runge_kutta



def test_newton_raphson():
    print("\n===== NEWTON RAPHSON =====")

    # Aquí puedes cambiar la función de prueba para verificar 
    # diferentes casos, puedes manipular o eliminar las variables que desees para 
    # probar la validación de parámetros faltantes.

    f = lambda x: x**2 - 2  # función de prueba: f(x) = x^2 - 2, cuya raíz es sqrt(2)
    f = lambda x: x**2 - 4  # función de prueba: f(x) = x^2 - 4
    f = lambda x: sp.sin(x)  # función de prueba: f(x) = sin(x), cuya raíz es 0
    f = lambda x: sp.cos(x) - x  # función de prueba: f(x) = cos(x) - x, cuya raíz es aproximadamente 0.7
    f= lambda x: sp.log(x) - 1  # función de prueba: f(x) = log(x) - 1, cuya raíz es e (aproximadamente 2.71828)    
    resultado = newton_raphson(f, 1.0)

    if resultado is None:
        print("No se encontró raíz.")
    else:
        root, historial = resultado
        print("Raíz encontrada:", root)
        print("Historial de iteraciones:")
        for i, val in enumerate(historial):
            print(f"iter {i}: {val}")

            

def test_euler():
    """Prueba del método de Euler."""
    def f(x, y):
        return x - y

    # Ejecutar el método de Euler mejorado con los parámetros de prueba
    # Aquí puedes ajustar los parámetros para hacer pruebas 
    x_values, y_values = euler_mejorado(f, 1,  0, 0.1, 12)

    if x_values is None or y_values is None:
        print("No se pudo ejecutar Euler mejorado por falta de parámetros")
        return

    print("Resultados del método de Euler mejorado:")
    for i in range(len(x_values)):
        print(f"x={x_values[i]}, y={y_values[i]}")

def test_runge_kutta():

    
    """Prueba del método de Runge-Kutta."""
    def f(x, y):
        return x + y
    
    # Ejecutar el método de Runge-Kutta con los parámetros de prueba
    # Aquí puedes ajustar los parámetros para hacer pruebas
    x_values, y_values = runge_kutta(f, 1, 0, 0.1, 12)

    if x_values is None or y_values is None:
        print("No se pudo ejecutar Runge-Kutta por falta de parámetros")
        return

    print("Resultados del método de Runge-Kutta:")
    for i in range(len(x_values)):
        print(f"x={x_values[i]}, y={y_values[i]}")


if __name__ == "__main__":
    test_newton_raphson()


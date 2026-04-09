import sympy as sp
from metodos.newton_raphson import newton_raphson
from metodos.euler import euler_mejorado
from metodos.runge_kutta import runge_kutta



def test_newton_raphson():
    print("\n===== NEWTON RAPHSON =====")

    f = lambda x: x**2 - 2
    f = lambda x: x**2 - 4
    f = lambda x: sp.sin(x)
    f = lambda x: sp.cos(x) - x
    f= lambda x: sp.log(x) - 1
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
    def f(x, y):
        return x - y

    x_values, y_values = euler_mejorado(f, 1,  0, 0.1, 12)

    if x_values is None or y_values is None:
        print("No se pudo ejecutar Euler mejorado por falta de parámetros")
        return

    print("Resultados del método de Euler mejorado:")
    for i in range(len(x_values)):
        print(f"x={x_values[i]}, y={y_values[i]}")

def test_runge_kutta():


    def f(x, y):
        return x + y

    x_values, y_values = runge_kutta(f, 1, 0, 0.1, 12)

    if x_values is None or y_values is None:
        print("No se pudo ejecutar Runge-Kutta por falta de parámetros")
        return

    print("Resultados del método de Runge-Kutta:")
    for i in range(len(x_values)):
        print(f"x={x_values[i]}, y={y_values[i]}")


if __name__ == "__main__":
    test_newton_raphson()


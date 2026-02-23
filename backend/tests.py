#Este es un archivo temporal para probar los métodos de Euler y Runge-Kutta. 
# No es un test unitario formal, sino una prueba rápida para verificar que los 
# métodos funcionan con una función simple.


from metodos.euler import euler_mejorado
from metodos.runge_kutta import runge_kutta

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
    test_euler()
    test_runge_kutta()



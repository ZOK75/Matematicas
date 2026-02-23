import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- CONFIGURACIÓN DE RUTAS ---
# Obtenemos la ruta de la carpeta 'backend'
backend_path = os.path.dirname(os.path.abspath(__file__))

# Añadimos 'utils' y 'metodos' al sistema para que Python los vea directamente
sys.path.append(os.path.join(backend_path, 'utils'))
sys.path.append(os.path.join(backend_path, 'metodos'))

# Ahora importamos los nombres de los ARCHIVOS directamente
try:
    # Importamos desde los archivos directamente (sin el punto de la carpeta)
    from validators import validate_all
    from parser import parse_function
    from newton_raphson import newton_raphson
    from euler import euler_mejorado
    from runge_kutta import runge_kutta
except ImportError as e:
    print(f"Error crítico de importación: {e}")
    print("Asegúrate de que los archivos existan en las carpetas utils/ y metodos/")
    sys.exit(1)

app = Flask(__name__)
CORS(app)


@app.route('/api/calcular', methods=['POST'])
def calcular():
    data = request.json
    metodo = data.get('metodo')
    params = data.get('params')

    try:
        # MÉTODO DE NEWTON-RAPHSON (VERSIÓN ANTIBALAS)
        if metodo == 'newton':
            import sympy as sp

            func_str = params['funcion'].replace('^', '**')
            x_sym = sp.symbols('x')

            try:
                # 1. Creamos la expresión y su derivada matemáticamente
                expr = sp.sympify(func_str)
                derivada = sp.diff(expr, x_sym)

                # 2. Creamos funciones que devuelven números REALES (float)
                # Usamos dict para asegurar que 'x' es la única variable
                def f_eval(val_x):
                    resultado = expr.subs({x_sym: val_x})
                    return float(resultado.evalf())

                def df_eval(val_x):
                    resultado = derivada.subs({x_sym: val_x})
                    return float(resultado.evalf())

                # 3. Tu amigo probablemente espera una función f(x)
                # Si su newton_raphson calcula la derivada internamente,
                # le pasamos esta función que es puro número:
                def f_final(val_x):
                    return f_eval(val_x)

                x0 = float(params['x0'])

                # Ejecutamos el algoritmo
                root, historial = newton_raphson(f_final, x0)

                return jsonify({
                    'root': float(root),
                    'x_values': list(range(len(historial))),
                    'y_values': [float(v) for v in historial]  # Aseguramos que todo sea float
                })
            except Exception as e:
                print(f"Error crítico en Newton: {e}")
                return jsonify({'error': f"Error de evaluación: {str(e)}"}), 400

        # MÉTODOS DE EULER Y RUNGE-KUTTA
        elif metodo in ['euler', 'runge_kutta']:
            # Aquí sí usamos el validador de los 5 parámetros
            f_calc, x0, y0, h, n = validate_all(
                params['funcion'],
                params['x0'],
                params['y0'],
                params['h'],
                params['n']
            )

            if metodo == 'euler':
                x_vals, y_vals = euler_mejorado(f_calc, x0, y0, h, n)
            else:
                x_vals, y_vals = runge_kutta(f_calc, x0, y0, h, n)

            return jsonify({'x_values': x_vals, 'y_values': y_vals})

    except Exception as e:
        # Si algo falla, imprimimos en la consola de Python para ver el error real
        print(f"Error en el servidor: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("--- Servidor de Métodos Numéricos ---")
    print("Escuchando en http://localhost:5000")
    app.run(debug=True, port=5000)
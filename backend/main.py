import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Obtenemos la ruta de la carpeta 'backend'
backend_path = os.path.dirname(os.path.abspath(__file__))

# Añadimos 'utils' y 'metodos' al sistema para que Python los vea directamente
sys.path.append(os.path.join(backend_path, 'utils'))
sys.path.append(os.path.join(backend_path, 'metodos'))

try:
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
        if metodo == 'newton':
            try:
                f_calc = parse_function(params['funcion'], metodo="newton")
                x0 = float(params['x0'])
                tol = float(params.get('tol', 1e-7))        # si no lo mandan, usa 1e-7

                root, historial = newton_raphson(f_calc, x0, tol=tol)

                return jsonify({
                    'root': float(root),
                    'x_values': list(range(len(historial))),
                    'y_values': [float(v) for v in historial]
                })
            except Exception as e:
                print(f"Error crítico en Newton: {e}")
                return jsonify({'error': f"Error de evaluación: {str(e)}"}), 400

        elif metodo in ['euler', 'runge_kutta']:
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
        print(f"Error en el servidor: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("--- Servidor de Métodos Numéricos ---")
    print("Escuchando en http://localhost:5000")
    app.run(debug=True, port=5000)

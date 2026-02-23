from flask import Flask, request, jsonify
from flask_cors import CORS
from metodos.newton_raphson import newton_raphson
from metodos.euler import euler_mejorado
from metodos.runge_kutta import runge_kutta
from utils.validators import validate_all, parse_function

app = Flask(__name__)
CORS(app)  # Esto permite que Vue (puerto 5173) hable con Python (puerto 5000)


@app.route('/api/calcular', methods=['POST'])
def calcular():
    data = request.json
    metodo = data.get('metodo')
    params = data.get('params')  # Aquí vienen funcion, x0, y0, h, n

    try:
        if metodo in ['euler', 'runge_kutta']:
            # 1. Validar usando el código de tu amigo
            f_calc, x0, y0, h, n = validate_all(
                params['funcion'], params['x0'], params['y0'], params['h'], params['n']
            )

            # 2. Ejecutar el método correspondiente
            if metodo == 'euler':
                x_vals, y_vals = euler_mejorado(f_calc, x0, y0, h, n)
            else:
                x_vals, y_vals = runge_kutta(f_calc, x0, y0, h, n)

            return jsonify({'x_values': x_vals, 'y_values': y_vals})

        elif metodo == 'newton':
            # Newton es especial porque solo usa x (tu amigo lo hizo con lambdify)
            # Crearemos una función compatible para su script
            f_calc = parse_function(params['funcion'])
            root, historial = newton_raphson(lambda x: f_calc(x, 0), float(params['x0']))

            return jsonify({'root': root, 'historial': historial})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
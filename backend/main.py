import sys
import os
# Eliminado: import webbrowser
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

dist_folder = os.path.abspath(os.path.join(base_path, 'dist'))

if not os.path.exists(dist_folder):
    print(f"ERROR FATAL: La carpeta 'dist' no se encuentra en: {dist_folder}")
elif not os.path.exists(os.path.join(dist_folder, 'index.html')):
    print(f"ERROR FATAL: No existe 'index.html' dentro de: {dist_folder}")
else:
    print(f"ÉXITO: Carpeta dist localizada en: {dist_folder}")

sys.path.append(os.path.join(base_path, 'utils'))
sys.path.append(os.path.join(base_path, 'metodos'))

try:
    from validators import validate_all
    from newton_raphson import newton_raphson
    from euler import euler_mejorado
    from runge_kutta import runge_kutta
except ImportError as e:
    print(f"Error crítico de importación: {e}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return send_from_directory(dist_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    full_path = os.path.join(dist_folder, path)
    if os.path.exists(full_path):
        return send_from_directory(dist_folder, path)
    return send_from_directory(dist_folder, 'index.html')

@app.route('/api/calcular', methods=['POST'])
def calcular():
    data = request.json
    metodo = data.get('metodo')
    params = data.get('params')
    try:
        if metodo == 'newton':
            root, historial = newton_raphson(params['funcion'], float(params['x0']), tol=float(params.get('tol', 1e-7)))
            return jsonify({'root': float(root), 'historial_completo': historial})
        elif metodo in ['euler', 'runge_kutta']:
            f_calc, x0, y0, h, n = validate_all(params['funcion'], params['x0'], params['y0'], params['h'], params['n'])
            if metodo == 'euler':
                x_vals, y_vals, detalles = euler_mejorado(f_calc, x0, y0, h, n)
                return jsonify({'x_values': x_vals, 'y_values': y_vals, 'detalles': detalles})
            else:
                x_vals, y_vals, ks = runge_kutta(f_calc, x0, y0, h, n)
                return jsonify({'x_values': x_vals, 'y_values': y_vals, 'ks': ks})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = 5000
    # Eliminado: Bloque de apertura de navegador
    print(f"--- Servidor listo en http://localhost:{port} ---")
    app.run(host='0.0.0.0', port=port, debug=False)
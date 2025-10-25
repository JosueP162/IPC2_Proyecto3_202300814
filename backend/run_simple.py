# [file name]: run_simple.py
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Rutas básicas de prueba
@app.route('/')
def home():
    return jsonify({
        'message': '✅ Backend funcionando',
        'status': 'success'
    })

@app.route('/api/test')
def test():
    return jsonify({'message': 'API test funcionando'})

# Importar y registrar solo las rutas que SÍ existen
try:
    from app.routes.recurso_routes import recurso_bp
    app.register_blueprint(recurso_bp, url_prefix='/api/recursos')
    print("✅ Rutas de recursos registradas")
except ImportError as e:
    print(f"⚠️  Rutas de recursos no disponibles: {e}")

try:
    from app.routes.categoria_routes import categoria_bp
    app.register_blueprint(categoria_bp, url_prefix='/api/categorias')
    print("✅ Rutas de categorías registradas")
except ImportError as e:
    print(f"⚠️  Rutas de categorías no disponibles: {e}")

try:
    from app.routes.cliente_routes import cliente_bp
    app.register_blueprint(cliente_bp, url_prefix='/api/clientes')
    print("✅ Rutas de clientes registradas")
except ImportError as e:
    print(f"⚠️  Rutas de clientes no disponibles: {e}")

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    print("📍 URL: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
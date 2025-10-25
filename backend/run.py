# [file name]: run_corregido.py
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': '✅ Backend funcionando', 'status': 'success'})

@app.route('/api/test')
def test():
    return jsonify({'test': '✅ Todo funciona correctamente'})

# Importar SOLO las rutas que existen y están correctas
try:
    from app.routes.recurso_routes import recurso_bp
    app.register_blueprint(recurso_bp, url_prefix='/api/recursos')
    print("✅ Rutas de recursos - REGISTRADAS")
except Exception as e:
    print(f"❌ Error recursos: {e}")

try:
    from app.routes.categoria_routes import categoria_bp
    app.register_blueprint(categoria_bp, url_prefix='/api/categorias')
    print("✅ Rutas de categorías - REGISTRADAS")
except Exception as e:
    print(f"❌ Error categorías: {e}")

try:
    from app.routes.cliente_routes import cliente_bp
    app.register_blueprint(cliente_bp, url_prefix='/api/clientes')
    print("✅ Rutas de clientes - REGISTRADAS")
except Exception as e:
    print(f"❌ Error clientes: {e}")

try:
    from app.routes.configuracion_routes import configuracion_bp
    app.register_blueprint(configuracion_bp, url_prefix='/api/configuraciones')
    print("✅ Rutas de configuración - REGISTRADAS")
except Exception as e:
    print(f"❌ Error configuraciones: {e}")

try:
    from app.routes.facturacion_routes import facturacion_bp
    app.register_blueprint(facturacion_bp, url_prefix='/api/facturacion')
    print("✅ Rutas de facturación - REGISTRADAS")
except Exception as e:
    print(f"❌ Error facturación: {e}")

try:
    from app.routes.sistema_routes import sistema_bp
    app.register_blueprint(sistema_bp, url_prefix='/api/sistema')
    print("✅ Rutas de sistema - REGISTRADAS")
except Exception as e:
    print(f"❌ Error sistema: {e}")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 BACKEND INICIADO CORRECTAMENTE")
    print("="*50)
    print("📍 URL: http://127.0.0.1:5000")
    print("📍 Test: http://127.0.0.1:5000/api/test")
    print("🛑 Ctrl+C para detener")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
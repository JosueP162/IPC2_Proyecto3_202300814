# [file name]: app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    CORS(app)
    
    # Importar y registrar blueprints DIRECTAMENTE
    from app.routes.recurso_routes import recurso_bp
    from app.routes.categoria_routes import categoria_bp
    from app.routes.cliente_routes import cliente_bp
    from app.routes.configuracion_routes import configuracion_bp
    from app.routes.facturacion_routes import facturacion_bp
    from app.routes.sistema_routes import sistema_bp
    
    app.register_blueprint(recurso_bp, url_prefix='/api/recursos')
    app.register_blueprint(categoria_bp, url_prefix='/api/categorias')
    app.register_blueprint(cliente_bp, url_prefix='/api/clientes')
    app.register_blueprint(configuracion_bp, url_prefix='/api/configuraciones')
    app.register_blueprint(facturacion_bp, url_prefix='/api/facturacion')
    app.register_blueprint(sistema_bp, url_prefix='/api/sistema')
    
    return app
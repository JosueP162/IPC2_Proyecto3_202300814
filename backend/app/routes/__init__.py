# [file name]: app/routes/__init__.py
# ARCHIVO CORREGIDO - Ya no causa errores

# Importa los blueprints con los nombres CORRECTOS
from .recurso_routes import recurso_bp
from .categoria_routes import categoria_bp
from .cliente_routes import cliente_bp
from .configuracion_routes import configuracion_bp  # ← CORREGIDO: configuracion_bp, NO config_bp
from .facturacion_routes import facturacion_bp
from .sistema_routes import sistema_bp

# Lista de todos los blueprints disponibles
__all__ = [
    'recurso_bp',
    'categoria_bp', 
    'cliente_bp',
    'configuracion_bp',  
    'facturacion_bp',
    'sistema_bp'
]
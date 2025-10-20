from .config_routes import config_bp
from .sistema_routes import consumo_bp
from .recurso_routes import recurso_bp
from .categoria_routes import categoria_bp
from .cliente_routes import cliente_bp
from .facturacion_routes import facturacion_bp

__all__ = [
    'config_bp',
    'consumo_bp',
    'recurso_bp',
    'categoria_bp',
    'cliente_bp',
    'facturacion_bp'
]
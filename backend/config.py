# [file name]: app/config.py
import os

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-para-desarrollo'
    XML_DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'data.xml')
    TEMP_FOLDER = os.path.join(os.path.dirname(__file__), 'temp')
    
    # Configuración de reportes PDF
    PDF_REPORTS_FOLDER = os.path.join(os.path.dirname(__file__), 'reports')
    
    # Crear carpetas si no existen
    @staticmethod
    def init_folders():
        folders = [Config.TEMP_FOLDER, Config.PDF_REPORTS_FOLDER]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
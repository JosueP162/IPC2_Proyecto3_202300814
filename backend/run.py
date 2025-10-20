# [file name]: run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Accesible desde cualquier IP
        port=5000,       # Puerto estándar
        debug=True,      # Modo desarrollo
        threaded=True    # Manejar múltiples peticiones
    )
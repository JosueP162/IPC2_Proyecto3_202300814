# [file name]: copiar_adminlte_windows.py
import os
import shutil
from pathlib import Path

def copiar_adminlte_windows():
    print("📁 Copiando AdminLTE a static...")
    
    # Rutas base
    node_modules = Path('node_modules')
    static_dir = Path('static/admin-lte')
    
    # Crear directorio static si no existe
    static_dir.mkdir(parents=True, exist_ok=True)
    
    # Solo copiar lo que SÍ existe
    archivos_a_intentar = [
        # AdminLTE
        ('admin-lte/dist/css/adminlte.min.css', 'dist/css/adminlte.min.css'),
        ('admin-lte/dist/js/adminlte.min.js', 'dist/js/adminlte.min.js'),
        
        # Bootstrap (si existen)
        ('bootstrap/dist/css/bootstrap.min.css', 'plugins/bootstrap/css/bootstrap.min.css'),
        ('bootstrap/dist/js/bootstrap.bundle.min.js', 'plugins/bootstrap/js/bootstrap.bundle.min.js'),
        
        # jQuery (si existe)
        ('jquery/dist/jquery.min.js', 'plugins/jquery/jquery.min.js'),
    ]
    
    for origen_rel, destino_rel in archivos_a_intentar:
        origen_path = node_modules / origen_rel
        destino_path = static_dir / destino_rel
        
        # Crear directorio de destino
        destino_path.parent.mkdir(parents=True, exist_ok=True)
        
        if origen_path.exists():
            try:
                shutil.copy2(origen_path, destino_path)
                print(f"✅ Copiado: {origen_rel} → {destino_rel}")
            except Exception as e:
                print(f"❌ Error copiando {origen_rel}: {e}")
        else:
            print(f"⚠️  No existe: {origen_rel}")
    
    print("\n🎉 Proceso completado!")

if __name__ == '__main__':
    copiar_adminlte_windows()
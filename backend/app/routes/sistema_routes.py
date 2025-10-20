# [file name]: app/routes/sistema_routes.py
from flask import Blueprint, request, jsonify
from app.database.xml_manager import XMLManager
from app.services.xml_procesor import XMLConfigProcessor, XMLConsumoProcessor

sistema_bp = Blueprint('sistema', __name__)
xml_manager = XMLManager()

@sistema_bp.route('/inicializar', methods=['POST'])
def inicializar_sistema():
    """Inicializa el sistema eliminando todos los datos"""
    try:
        xml_manager.limpiar_database()
        return jsonify({
            'success': True,
            'message': 'Sistema inicializado exitosamente. Todos los datos han sido eliminados.'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al inicializar sistema: {str(e)}'
        }), 500

@sistema_bp.route('/cargar-configuracion', methods=['POST'])
def cargar_configuracion_xml():
    """Carga datos de configuración desde XML"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No se proporcionó archivo XML'
            }), 400
        
        archivo = request.files['file']
        if archivo.filename == '':
            return jsonify({
                'success': False,
                'message': 'No se seleccionó ningún archivo'
            }), 400
        
        if not archivo.filename.endswith('.xml'):
            return jsonify({
                'success': False,
                'message': 'El archivo debe ser XML'
            }), 400
        
        xml_content = archivo.read().decode('utf-8')
        processor = XMLConfigProcessor(xml_content)
        resultado = processor.procesar()
        
        # Guardar los objetos procesados en la base de datos
        for recurso in processor.recursos:
            xml_manager.guardar_recurso(recurso)
        
        for categoria in processor.categorias:
            xml_manager.guardar_categoria(categoria)
        
        for cliente in processor.clientes:
            xml_manager.guardar_cliente(cliente)
        
        return jsonify({
            'success': True,
            'message': 'Configuración XML procesada exitosamente',
            'data': resultado
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al procesar configuración XML: {str(e)}'
        }), 500

@sistema_bp.route('/cargar-consumos', methods=['POST'])
def cargar_consumos_xml():
    """Carga consumos desde XML"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No se proporcionó archivo XML'
            }), 400
        
        archivo = request.files['file']
        if archivo.filename == '':
            return jsonify({
                'success': False,
                'message': 'No se seleccionó ningún archivo'
            }), 400
        
        if not archivo.filename.endswith('.xml'):
            return jsonify({
                'success': False,
                'message': 'El archivo debe ser XML'
            }), 400
        
        xml_content = archivo.read().decode('utf-8')
        processor = XMLConsumoProcessor(xml_content)
        resultado = processor.procesar()
        
        # Guardar los consumos procesados
        for consumo in processor.consumos:
            xml_manager.guardar_consumo(consumo)
        
        return jsonify({
            'success': True,
            'message': 'Consumos XML procesados exitosamente',
            'data': resultado
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al procesar consumos XML: {str(e)}'
        }), 500

@sistema_bp.route('/estado', methods=['GET'])
def obtener_estado_sistema():
    """Obtiene el estado actual del sistema"""
    try:
        recursos = xml_manager.obtener_recursos()
        categorias = xml_manager.obtener_categorias()
        clientes = xml_manager.obtener_clientes()
        facturas = xml_manager.obtener_facturas()
        
        return jsonify({
            'success': True,
            'data': {
                'recursos': len(recursos),
                'categorias': len(categorias),
                'clientes': len(clientes),
                'facturas': len(facturas),
                'instancias_activas': sum(len(cliente.instancias) for cliente in clientes),
                'total_instancias': sum(len(cliente.instancias) for cliente in clientes)
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener estado del sistema: {str(e)}'
        }), 500

@sistema_bp.route('/exportar-datos', methods=['GET'])
def exportar_datos():
    """Exporta todos los datos del sistema a XML"""
    try:
        xml_data = xml_manager.exportar_todo_a_xml()
        
        return jsonify({
            'success': True,
            'data': xml_data,
            'message': 'Datos exportados exitosamente'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al exportar datos: {str(e)}'
        }), 500
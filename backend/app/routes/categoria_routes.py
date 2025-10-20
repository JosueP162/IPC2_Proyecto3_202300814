# [file name]: app/routes/categoria_routes.py
from flask import Blueprint, request, jsonify
from app.services.categoria_service import CategoriaService

categoria_bp = Blueprint('categoria', __name__)
categoria_service = CategoriaService()

@categoria_bp.route('/', methods=['GET'])
def obtener_categorias():
    """Obtiene todas las categorías con sus configuraciones"""
    try:
        incluir_configuraciones = request.args.get('incluir_configuraciones', 'true').lower() == 'true'
        categorias = categoria_service.obtener_todas()
        
        return jsonify({
            'success': True,
            'data': [cat.to_dict(incluir_configuraciones) for cat in categorias],
            'total': len(categorias)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener categorías: {str(e)}'
        }), 500

@categoria_bp.route('/<int:id_categoria>', methods=['GET'])
def obtener_categoria(id_categoria):
    """Obtiene una categoría por ID"""
    try:
        categoria = categoria_service.obtener_por_id(id_categoria)
        if categoria:
            return jsonify({
                'success': True,
                'data': categoria.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Categoría con ID {id_categoria} no encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener categoría: {str(e)}'
        }), 500

@categoria_bp.route('/', methods=['POST'])
def crear_categoria():
    """Crea una nueva categoría"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos JSON'
            }), 400
        
        campos_requeridos = ['id', 'nombre', 'descripcion', 'carga_trabajo']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido faltante: {campo}'
                }), 400
        
        categoria = categoria_service.crear_categoria(datos)
        return jsonify({
            'success': True,
            'message': 'Categoría creada exitosamente',
            'data': categoria.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear categoría: {str(e)}'
        }), 500

@categoria_bp.route('/<int:id_categoria>/configuraciones', methods=['POST'])
def agregar_configuracion(id_categoria):
    """Agrega una configuración a una categoría"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos JSON'
            }), 400
        
        campos_requeridos = ['id', 'nombre', 'descripcion']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido faltante: {campo}'
                }), 400
        
        # Asegurar que recursos sea un diccionario
        if 'recursos' not in datos:
            datos['recursos'] = {}
        
        configuracion = categoria_service.agregar_configuracion(id_categoria, datos)
        return jsonify({
            'success': True,
            'message': 'Configuración agregada exitosamente',
            'data': configuracion.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al agregar configuración: {str(e)}'
        }), 500

@categoria_bp.route('/configuraciones/<int:id_configuracion>', methods=['PUT'])
def actualizar_configuracion(id_configuracion):
    """Actualiza una configuración existente"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos JSON'
            }), 400
        
        configuracion = categoria_service.actualizar_configuracion(id_configuracion, datos)
        return jsonify({
            'success': True,
            'message': 'Configuración actualizada exitosamente',
            'data': configuracion.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar configuración: {str(e)}'
        }), 500

@categoria_bp.route('/configuraciones/<int:id_configuracion>', methods=['DELETE'])
def eliminar_configuracion(id_configuracion):
    """Elimina una configuración"""
    try:
        eliminado = categoria_service.eliminar_configuracion(id_configuracion)
        if eliminado:
            return jsonify({
                'success': True,
                'message': 'Configuración eliminada exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Configuración no encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar configuración: {str(e)}'
        }), 500

@categoria_bp.route('/<int:id_categoria>', methods=['DELETE'])
def eliminar_categoria(id_categoria):
    """Elimina una categoría completa"""
    try:
        eliminado = categoria_service.eliminar_categoria(id_categoria)
        if eliminado:
            return jsonify({
                'success': True,
                'message': 'Categoría eliminada exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Categoría no encontrada'
            }), 404
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar categoría: {str(e)}'
        }), 500

@categoria_bp.route('/configuraciones/costos', methods=['GET'])
def obtener_configuraciones_con_costos():
    """Obtiene todas las configuraciones con sus costos por hora"""
    try:
        configuraciones = categoria_service.obtener_configuraciones_con_costos()
        return jsonify({
            'success': True,
            'data': configuraciones,
            'total': len(configuraciones)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener configuraciones: {str(e)}'
        }), 500
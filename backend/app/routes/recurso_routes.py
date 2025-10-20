# [file name]: app/routes/recurso_routes.py
from flask import Blueprint, request, jsonify
from app.services.recurso_service import RecursoService
from app.utils.validators import validar_tipo_recurso

recurso_bp = Blueprint('recurso', __name__)
recurso_service = RecursoService()

@recurso_bp.route('/', methods=['GET'])
def obtener_recursos():
    """Obtiene todos los recursos"""
    try:
        recursos = recurso_service.obtener_todos()
        return jsonify({
            'success': True,
            'data': [recurso.to_dict() for recurso in recursos],
            'total': len(recursos)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener recursos: {str(e)}'
        }), 500

@recurso_bp.route('/<int:id_recurso>', methods=['GET'])
def obtener_recurso(id_recurso):
    """Obtiene un recurso por ID"""
    try:
        recurso = recurso_service.obtener_por_id(id_recurso)
        if recurso:
            return jsonify({
                'success': True,
                'data': recurso.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Recurso con ID {id_recurso} no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener recurso: {str(e)}'
        }), 500

@recurso_bp.route('/', methods=['POST'])
def crear_recurso():
    """Crea un nuevo recurso"""
    try:
        datos = request.get_json()
        
        # Validaciones básicas
        if not datos:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos JSON'
            }), 400
        
        campos_requeridos = ['id', 'nombre', 'abreviatura', 'metrica', 'tipo', 'valor_x_hora']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido faltante: {campo}'
                }), 400
        
        # Validar tipo de recurso
        if not validar_tipo_recurso(datos['tipo']):
            return jsonify({
                'success': False,
                'message': 'Tipo de recurso inválido. Debe ser "Hardware" o "Software"'
            }), 400
        
        # Validar valor por hora
        if datos['valor_x_hora'] <= 0:
            return jsonify({
                'success': False,
                'message': 'El valor por hora debe ser mayor a 0'
            }), 400
        
        recurso = recurso_service.crear_recurso(datos)
        return jsonify({
            'success': True,
            'message': 'Recurso creado exitosamente',
            'data': recurso.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear recurso: {str(e)}'
        }), 500

@recurso_bp.route('/<int:id_recurso>', methods=['PUT'])
def actualizar_recurso(id_recurso):
    """Actualiza un recurso existente"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos JSON'
            }), 400
        
        # Validar tipo de recurso si se está actualizando
        if 'tipo' in datos and not validar_tipo_recurso(datos['tipo']):
            return jsonify({
                'success': False,
                'message': 'Tipo de recurso inválido. Debe ser "Hardware" o "Software"'
            }), 400
        
        # Validar valor por hora si se está actualizando
        if 'valor_x_hora' in datos and datos['valor_x_hora'] <= 0:
            return jsonify({
                'success': False,
                'message': 'El valor por hora debe ser mayor a 0'
            }), 400
        
        recurso = recurso_service.actualizar_recurso(id_recurso, datos)
        return jsonify({
            'success': True,
            'message': 'Recurso actualizado exitosamente',
            'data': recurso.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar recurso: {str(e)}'
        }), 500

@recurso_bp.route('/<int:id_recurso>', methods=['DELETE'])
def eliminar_recurso(id_recurso):
    """Elimina un recurso"""
    try:
        # Verificar si el recurso existe antes de eliminar
        recurso = recurso_service.obtener_por_id(id_recurso)
        if not recurso:
            return jsonify({
                'success': False,
                'message': f'Recurso con ID {id_recurso} no encontrado'
            }), 404
        
        # Verificar si el recurso está siendo usado en alguna configuración
        from app.services.categoria_service import CategoriaService
        categoria_service = CategoriaService()
        configuraciones = categoria_service.obtener_configuraciones_con_costos()
        
        for config in configuraciones:
            if id_recurso in config['recursos']:
                return jsonify({
                    'success': False,
                    'message': f'No se puede eliminar el recurso. Está siendo usado en la configuración {config["configuracion_nombre"]}'
                }), 400
        
        eliminado = recurso_service.eliminar_recurso(id_recurso)
        if eliminado:
            return jsonify({
                'success': True,
                'message': 'Recurso eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error al eliminar el recurso'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar recurso: {str(e)}'
        }), 500
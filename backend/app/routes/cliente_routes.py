# [file name]: app/routes/cliente_routes.py
from flask import Blueprint, request, jsonify
from app.services.cliente_service import ClienteService
from app.utils.regex_utils import validar_nit
from app.utils.validators import validar_estado_instancia, validar_fecha

cliente_bp = Blueprint('cliente', __name__)
cliente_service = ClienteService()

@cliente_bp.route('/', methods=['GET'])
def obtener_clientes():
    """Obtiene todos los clientes con sus instancias"""
    try:
        clientes = cliente_service.obtener_todos()
        return jsonify({
            'success': True,
            'data': [cliente.to_dict() for cliente in clientes],
            'total': len(clientes)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener clientes: {str(e)}'
        }), 500

@cliente_bp.route('/<string:nit>', methods=['GET'])
def obtener_cliente(nit):
    """Obtiene un cliente por NIT"""
    try:
        cliente = cliente_service.obtener_por_nit(nit)
        if cliente:
            return jsonify({
                'success': True,
                'data': cliente.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Cliente con NIT {nit} no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener cliente: {str(e)}'
        }), 500

@cliente_bp.route('/', methods=['POST'])
def crear_cliente():
    """Crea un nuevo cliente"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos JSON'
            }), 400
        
        campos_requeridos = ['nit', 'nombre', 'usuario', 'clave', 'direccion', 'correo_electronico']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido faltante: {campo}'
                }), 400
        
        # Validar NIT
        if not validar_nit(datos['nit']):
            return jsonify({
                'success': False,
                'message': 'Formato de NIT inválido. Debe ser: dígitos-[0-9K]'
            }), 400
        
        cliente = cliente_service.crear_cliente(datos)
        return jsonify({
            'success': True,
            'message': 'Cliente creado exitosamente',
            'data': cliente.to_dict(incluir_instancias=False)
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear cliente: {str(e)}'
        }), 500

@cliente_bp.route('/<string:nit>/instancias', methods=['POST'])
def agregar_instancia(nit):
    """Agrega una instancia a un cliente"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos JSON'
            }), 400
        
        campos_requeridos = ['id', 'id_configuracion', 'nombre', 'fecha_inicio', 'estado']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido faltante: {campo}'
                }), 400
        
        # Validar estado de instancia
        if not validar_estado_instancia(datos['estado']):
            return jsonify({
                'success': False,
                'message': 'Estado de instancia inválido. Debe ser "Vigente" o "Cancelada"'
            }), 400
        
        # Validar fecha de inicio
        if not validar_fecha(datos['fecha_inicio']):
            return jsonify({
                'success': False,
                'message': 'Formato de fecha inválido. Use dd/mm/yyyy'
            }), 400
        
        # Validar fecha final si se proporciona
        if 'fecha_final' in datos and datos['fecha_final'] and not validar_fecha(datos['fecha_final']):
            return jsonify({
                'success': False,
                'message': 'Formato de fecha final inválido. Use dd/mm/yyyy'
            }), 400
        
        instancia = cliente_service.agregar_instancia(nit, datos)
        return jsonify({
            'success': True,
            'message': 'Instancia agregada exitosamente',
            'data': instancia.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al agregar instancia: {str(e)}'
        }), 500

@cliente_bp.route('/<string:nit>/instancias/<int:id_instancia>/cancelar', methods=['PUT'])
def cancelar_instancia(nit, id_instancia):
    """Cancela una instancia de un cliente"""
    try:
        datos = request.get_json()
        
        if not datos or 'fecha_final' not in datos:
            return jsonify({
                'success': False,
                'message': 'Se requiere la fecha final para cancelar la instancia'
            }), 400
        
        # Validar fecha final
        if not validar_fecha(datos['fecha_final']):
            return jsonify({
                'success': False,
                'message': 'Formato de fecha final inválido. Use dd/mm/yyyy'
            }), 400
        
        instancia = cliente_service.cancelar_instancia(nit, id_instancia, datos['fecha_final'])
        return jsonify({
            'success': True,
            'message': 'Instancia cancelada exitosamente',
            'data': instancia.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al cancelar instancia: {str(e)}'
        }), 500

@cliente_bp.route('/<string:nit>', methods=['DELETE'])
def eliminar_cliente(nit):
    """Elimina un cliente"""
    try:
        eliminado = cliente_service.eliminar_cliente(nit)
        if eliminado:
            return jsonify({
                'success': True,
                'message': 'Cliente eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Cliente no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al eliminar cliente: {str(e)}'
        }), 500
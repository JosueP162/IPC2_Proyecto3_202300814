# [file name]: app/routes/configuracion_routes.py
from flask import Blueprint, request, jsonify
from app.services.categoria_service import CategoriaService

configuracion_bp = Blueprint('configuracion', __name__)
categoria_service = CategoriaService()

@configuracion_bp.route('/<int:id_configuracion>', methods=['GET'])
def obtener_configuracion(id_configuracion):
    """Obtiene una configuración por ID"""
    try:
        configuracion = categoria_service.obtener_configuracion_por_id(id_configuracion)
        if configuracion:
            return jsonify({
                'success': True,
                'data': configuracion.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Configuración con ID {id_configuracion} no encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener configuración: {str(e)}'
        }), 500

@configuracion_bp.route('/<int:id_configuracion>/validar', methods=['GET'])
def validar_configuracion(id_configuracion):
    """Valida que una configuración tenga todos sus recursos disponibles"""
    try:
        resultado = categoria_service.validar_configuracion(id_configuracion)
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al validar configuración: {str(e)}'
        }), 500
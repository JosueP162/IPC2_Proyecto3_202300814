# [file name]: app/routes/facturacion_routes.py
from flask import Blueprint, request, jsonify
from app.services.facturacion_service import FacturacionService
from app.utils.validators import validar_rango_fechas

facturacion_bp = Blueprint('facturacion', __name__)
facturacion_service = FacturacionService()

@facturacion_bp.route('/generar', methods=['POST'])
def generar_facturas():
    """Genera facturas para un rango de fechas"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos JSON'
            }), 400
        
        campos_requeridos = ['fecha_inicio', 'fecha_fin']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido faltante: {campo}'
                }), 400
        
        # Validar rango de fechas
        if not validar_rango_fechas(datos['fecha_inicio'], datos['fecha_fin']):
            return jsonify({
                'success': False,
                'message': 'Rango de fechas inválido. La fecha de inicio debe ser menor o igual a la fecha fin'
            }), 400
        
        facturas = facturacion_service.generar_facturas(
            datos['fecha_inicio'], 
            datos['fecha_fin']
        )
        
        return jsonify({
            'success': True,
            'message': f'Se generaron {len(facturas)} facturas exitosamente',
            'data': [factura.to_dict() for factura in facturas],
            'total': len(facturas)
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al generar facturas: {str(e)}'
        }), 500

@facturacion_bp.route('/', methods=['GET'])
def obtener_facturas():
    """Obtiene todas las facturas o las de un cliente específico"""
    try:
        nit_cliente = request.args.get('nit_cliente')
        facturas = facturacion_service.obtener_facturas(nit_cliente)
        
        return jsonify({
            'success': True,
            'data': [factura.to_dict() for factura in facturas],
            'total': len(facturas)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener facturas: {str(e)}'
        }), 500

@facturacion_bp.route('/<int:numero>', methods=['GET'])
def obtener_factura(numero):
    """Obtiene una factura por su número"""
    try:
        factura = facturacion_service.obtener_factura_por_numero(numero)
        if factura:
            return jsonify({
                'success': True,
                'data': factura.to_dict(incluir_detalles=True)
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Factura número {numero} no encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener factura: {str(e)}'
        }), 500

@facturacion_bp.route('/analisis/categorias', methods=['GET'])
def analizar_ventas_por_categoria():
    """Analiza las ventas por categoría en un rango de fechas"""
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({
                'success': False,
                'message': 'Se requieren los parámetros fecha_inicio y fecha_fin'
            }), 400
        
        # Validar rango de fechas
        if not validar_rango_fechas(fecha_inicio, fecha_fin):
            return jsonify({
                'success': False,
                'message': 'Rango de fechas inválido'
            }), 400
        
        resultado = facturacion_service.analizar_ventas_por_categoria(fecha_inicio, fecha_fin)
        
        return jsonify({
            'success': True,
            'data': resultado,
            'total': len(resultado)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al analizar ventas por categoría: {str(e)}'
        }), 500

@facturacion_bp.route('/analisis/recursos', methods=['GET'])
def analizar_ventas_por_recurso():
    """Analiza las ventas por recurso en un rango de fechas"""
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({
                'success': False,
                'message': 'Se requieren los parámetros fecha_inicio y fecha_fin'
            }), 400
        
        # Validar rango de fechas
        if not validar_rango_fechas(fecha_inicio, fecha_fin):
            return jsonify({
                'success': False,
                'message': 'Rango de fechas inválido'
            }), 400
        
        resultado = facturacion_service.analizar_ventas_por_recurso(fecha_inicio, fecha_fin)
        
        return jsonify({
            'success': True,
            'data': resultado,
            'total': len(resultado)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al analizar ventas por recurso: {str(e)}'
        }), 500

@facturacion_bp.route('/consumos-pendientes', methods=['GET'])
def obtener_consumos_pendientes():
    """Obtiene los consumos pendientes de facturar"""
    try:
        nit_cliente = request.args.get('nit_cliente')
        resultado = facturacion_service.obtener_consumos_pendientes(nit_cliente)
        
        return jsonify({
            'success': True,
            'data': resultado
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener consumos pendientes: {str(e)}'
        }), 500

@facturacion_bp.route('/resumen', methods=['GET'])
def obtener_resumen_facturacion():
    """Obtiene un resumen general de la facturación"""
    try:
        resumen = facturacion_service.obtener_resumen_facturacion()
        
        return jsonify({
            'success': True,
            'data': resumen
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener resumen de facturación: {str(e)}'
        }), 500
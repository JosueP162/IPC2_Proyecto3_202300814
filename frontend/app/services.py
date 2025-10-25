# [file name]: app/services.py
import requests
import json
from django.conf import settings

class BackendService:
    BASE_URL = settings.BACKEND_URL
    
    @staticmethod
    def _make_request(method, endpoint, data=None):
        try:
            url = f"{BackendService.BASE_URL}/{endpoint}"
            headers = {'Content-Type': 'application/json'}
            
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            
            if response.status_code == 200:
                return response.json() if response.content else {'success': True}
            else:
                return {'success': False, 'message': f'Error {response.status_code}'}
                
        except requests.exceptions.ConnectionError:
            return {'success': False, 'message': 'No se puede conectar al backend Flask'}
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    # Recursos
    @staticmethod
    def obtener_recursos():
        return BackendService._make_request('GET', 'recursos/')
    
    @staticmethod
    def crear_recurso(datos):
        return BackendService._make_request('POST', 'recursos/', datos)
    
    # Categorías
    @staticmethod
    def obtener_categorias():
        return BackendService._make_request('GET', 'categorias/')
    
    @staticmethod
    def crear_categoria(datos):
        return BackendService._make_request('POST', 'categorias/', datos)
    
    @staticmethod
    def agregar_configuracion(id_categoria, datos):
        return BackendService._make_request('POST', f'categorias/{id_categoria}/configuraciones', datos)
    
    # Clientes
    @staticmethod
    def obtener_clientes():
        return BackendService._make_request('GET', 'clientes/')
    
    @staticmethod
    def crear_cliente(datos):
        return BackendService._make_request('POST', 'clientes/', datos)
    
    @staticmethod
    def agregar_instancia(nit_cliente, datos):
        return BackendService._make_request('POST', f'clientes/{nit_cliente}/instancias', datos)
    
    @staticmethod
    def cancelar_instancia(nit_cliente, id_instancia, fecha_final):
        datos = {'fecha_final': fecha_final}
        return BackendService._make_request('PUT', f'clientes/{nit_cliente}/instancias/{id_instancia}/cancelar', datos)
    
    # Sistema
    @staticmethod
    def inicializar_sistema():
        return BackendService._make_request('POST', 'sistema/inicializar')
    
    @staticmethod
    def cargar_configuracion_xml(archivo):
        try:
            url = f"{BackendService.BASE_URL}/sistema/cargar-configuracion"
            files = {'file': archivo}
            response = requests.post(url, files=files)
            return response.json()
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    @staticmethod
    def cargar_consumos_xml(archivo):
        try:
            url = f"{BackendService.BASE_URL}/sistema/cargar-consumos"
            files = {'file': archivo}
            response = requests.post(url, files=files)
            return response.json()
        except Exception as e:
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    @staticmethod
    def obtener_estado_sistema():
        return BackendService._make_request('GET', 'sistema/estado')
    
    # Facturación
    @staticmethod
    def generar_facturas(fecha_inicio, fecha_fin):
        datos = {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        return BackendService._make_request('POST', 'facturacion/generar', datos)
    
    @staticmethod
    def obtener_facturas():
        return BackendService._make_request('GET', 'facturacion/')
    
    @staticmethod
    def obtener_factura(numero):
        return BackendService._make_request('GET', f'facturacion/{numero}')
    
    @staticmethod
    def analizar_ventas_categoria(fecha_inicio, fecha_fin):
        return BackendService._make_request('GET', f'facturacion/analisis/categorias?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}')
    
    @staticmethod
    def analizar_ventas_recurso(fecha_inicio, fecha_fin):
        return BackendService._make_request('GET', f'facturacion/analisis/recursos?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}')
    
    @staticmethod
    def obtener_consumos_pendientes():
        return BackendService._make_request('GET', 'facturacion/consumos-pendientes')
from datetime import datetime
from app.database.xml_manager import XMLManager
from app.models import Factura, DetalleFactura

class FacturacionService:
    """Servicio para gestionar la facturación y análisis de ventas."""
    
    def __init__(self, xml_manager=None):
        self.xml_manager = xml_manager or XMLManager()
    
    def generar_facturas(self, fecha_inicio, fecha_fin):
        """
        Genera facturas para todos los clientes en un rango de fechas.
        Solo factura consumos que NO han sido facturados previamente.
        
        Args:
            fecha_inicio (str): Fecha inicio en formato dd/mm/yyyy
            fecha_fin (str): Fecha fin en formato dd/mm/yyyy
            
        Returns:
            list: Lista de facturas generadas
            
        Raises:
            ValueError: Si el formato de fechas es inválido o rango inválido
        """
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio, '%d/%m/%Y')
            fecha_fin_obj = datetime.strptime(fecha_fin, '%d/%m/%Y')
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use dd/mm/yyyy")
        
        if fecha_inicio_obj > fecha_fin_obj:
            raise ValueError("La fecha de inicio debe ser menor o igual a la fecha fin")
        
        clientes = self.xml_manager.obtener_clientes()
        recursos_dict = {r.id: r for r in self.xml_manager.obtener_recursos()}
        
        facturas_generadas = []
        
        for cliente in clientes:
            factura = self._generar_factura_cliente(
                cliente, 
                fecha_inicio_obj, 
                fecha_fin_obj, 
                recursos_dict
            )
            
            if factura and factura.monto_total > 0:
                self.xml_manager.guardar_factura(factura)
                facturas_generadas.append(factura)
        
        return facturas_generadas
    
    def _generar_factura_cliente(self, cliente, fecha_inicio, fecha_fin, recursos_dict):
        """
        Genera una factura para un cliente específico.
        
        Args:
            cliente (Cliente): Cliente a facturar
            fecha_inicio (datetime): Fecha inicio
            fecha_fin (datetime): Fecha fin
            recursos_dict (dict): Diccionario de recursos {id: Recurso}
            
        Returns:
            Factura: Factura generada o None si no hay consumos
        """
        numero_factura = self.xml_manager.obtener_siguiente_numero_factura()
        factura = Factura(
            numero=numero_factura,
            nit_cliente=cliente.nit,
            fecha=fecha_fin.strftime('%d/%m/%Y'),
            monto_total=0.0
        )
        
        for instancia in cliente.instancias:
            detalle = self._procesar_instancia(
                instancia, 
                fecha_inicio, 
                fecha_fin, 
                recursos_dict
            )
            
            if detalle and detalle.costo_total > 0:
                factura.agregar_detalle(detalle)
        
        # Guardar cliente con consumos marcados como facturados
        if factura.monto_total > 0:
            self.xml_manager.guardar_cliente(cliente)
        
        return factura
    
    def _procesar_instancia(self, instancia, fecha_inicio, fecha_fin, recursos_dict):
        """
        Procesa una instancia y genera su detalle de factura.
        
        Args:
            instancia (Instancia): Instancia a procesar
            fecha_inicio (datetime): Fecha inicio
            fecha_fin (datetime): Fecha fin
            recursos_dict (dict): Diccionario de recursos
            
        Returns:
            DetalleFactura: Detalle generado o None si no hay consumos
        """
        horas_totales = 0.0
        consumos_procesados = []
        
        # Filtrar consumos en el rango y no facturados
        for consumo in instancia.consumos:
            if consumo.facturado:
                continue
            
            # Verificar si el consumo está en el rango de fechas
            if consumo.fecha_hora:
                try:
                    fecha_consumo = datetime.strptime(consumo.fecha_hora, '%d/%m/%Y %H:%M')
                    if fecha_inicio <= fecha_consumo <= fecha_fin:
                        horas_totales += consumo.tiempo
                        consumos_procesados.append(consumo)
                except ValueError:
                    # Si hay error parseando fecha, intentar solo con fecha
                    try:
                        fecha_consumo = datetime.strptime(consumo.fecha_hora.split()[0], '%d/%m/%Y')
                        if fecha_inicio <= fecha_consumo <= fecha_fin:
                            horas_totales += consumo.tiempo
                            consumos_procesados.append(consumo)
                    except:
                        continue
        
        if horas_totales == 0:
            return None
        
        # Obtener la configuración de la instancia
        configuracion = self.xml_manager.obtener_configuracion_por_id(instancia.id_configuracion)
        if not configuracion:
            return None
        
        detalle = DetalleFactura(
            id_instancia=instancia.id,
            nombre_instancia=instancia.nombre,
            horas_consumidas=horas_totales,
            costo_total=0.0
        )
        
        # Calcular costo por cada recurso de la configuración
        for id_recurso, cantidad in configuracion.recursos_config.items():
            if id_recurso in recursos_dict:
                recurso = recursos_dict[id_recurso]
                costo_recurso = recurso.calcular_costo(horas_totales, cantidad)
                
                detalle.agregar_detalle_recurso(
                    recurso_nombre=recurso.nombre,
                    cantidad=cantidad,
                    horas=horas_totales,
                    costo=costo_recurso
                )
                
                detalle._costo_total += costo_recurso
        
        # Marcar consumos como facturados
        for consumo in consumos_procesados:
            consumo.facturado = True
        
        return detalle
    
    def obtener_facturas(self, nit_cliente=None):
        """
        Obtiene todas las facturas o las de un cliente específico.
        
        Args:
            nit_cliente (str, optional): NIT del cliente
            
        Returns:
            list: Lista de facturas
        """
        if nit_cliente:
            return self.xml_manager.obtener_facturas_por_cliente(nit_cliente)
        return self.xml_manager.obtener_facturas()
    
    def obtener_factura_por_numero(self, numero):
        """
        Obtiene una factura por su número.
        
        Args:
            numero (int): Número de factura
            
        Returns:
            Factura: Factura encontrada o None
        """
        return self.xml_manager.obtener_factura_por_numero(numero)
    
    def analizar_ventas_por_categoria(self, fecha_inicio, fecha_fin):
        """
        Analiza las ventas por categoría y configuración en un rango de fechas.
        
        Args:
            fecha_inicio (str): Fecha inicio en formato dd/mm/yyyy
            fecha_fin (str): Fecha fin en formato dd/mm/yyyy
            
        Returns:
            list: Lista ordenada por ingresos descendente
        """
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio, '%d/%m/%Y')
            fecha_fin_obj = datetime.strptime(fecha_fin, '%d/%m/%Y')
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use dd/mm/yyyy")
        
        facturas = self.xml_manager.obtener_facturas()
        categorias = self.xml_manager.obtener_categorias()
        
        # Filtrar facturas en el rango
        facturas_rango = []
        for f in facturas:
            try:
                fecha_factura = datetime.strptime(f.fecha, '%d/%m/%Y')
                if fecha_inicio_obj <= fecha_factura <= fecha_fin_obj:
                    facturas_rango.append(f)
            except ValueError:
                continue
        
        # Crear mapeo de configuraciones a categorías
        config_to_cat = {}
        config_info = {}
        
        for categoria in categorias:
            for config in categoria.configuraciones:
                config_to_cat[config.id] = categoria
                config_info[config.id] = {
                    'categoria_id': categoria.id,
                    'categoria_nombre': categoria.nombre,
                    'configuracion_id': config.id,
                    'configuracion_nombre': config.nombre,
                    'ingresos': 0.0,
                    'instancias_vendidas': 0,
                    'horas_totales': 0.0
                }
        
        # Análisis por configuración
        for factura in facturas_rango:
            for detalle in factura.detalles:
                # Buscar la configuración de la instancia
                cliente = self.xml_manager.obtener_cliente_por_nit(factura.nit_cliente)
                if cliente:
                    instancia = cliente.obtener_instancia_por_id(detalle.id_instancia)
                    if instancia:
                        id_config = instancia.id_configuracion
                        
                        if id_config in config_info:
                            config_info[id_config]['ingresos'] += detalle.costo_total
                            config_info[id_config]['instancias_vendidas'] += 1
                            config_info[id_config]['horas_totales'] += detalle.horas_consumidas
        
        # Filtrar solo las que tienen ventas y ordenar
        resultado = [info for info in config_info.values() if info['ingresos'] > 0]
        resultado.sort(key=lambda x: x['ingresos'], reverse=True)
        
        # Redondear valores
        for item in resultado:
            item['ingresos'] = round(item['ingresos'], 2)
            item['horas_totales'] = round(item['horas_totales'], 2)
        
        return resultado
    
    def analizar_ventas_por_recurso(self, fecha_inicio, fecha_fin):
        """
        Analiza las ventas por recurso en un rango de fechas.
        
        Args:
            fecha_inicio (str): Fecha inicio en formato dd/mm/yyyy
            fecha_fin (str): Fecha fin en formato dd/mm/yyyy
            
        Returns:
            list: Lista ordenada por ingresos descendente
        """
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio, '%d/%m/%Y')
            fecha_fin_obj = datetime.strptime(fecha_fin, '%d/%m/%Y')
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use dd/mm/yyyy")
        
        facturas = self.xml_manager.obtener_facturas()
        
        # Filtrar facturas en el rango
        facturas_rango = []
        for f in facturas:
            try:
                fecha_factura = datetime.strptime(f.fecha, '%d/%m/%Y')
                if fecha_inicio_obj <= fecha_factura <= fecha_fin_obj:
                    facturas_rango.append(f)
            except ValueError:
                continue
        
        # Análisis por recurso
        analisis_recursos = {}
        
        for factura in facturas_rango:
            for detalle in factura.detalles:
                for detalle_recurso in detalle.detalles_recursos:
                    nombre_recurso = detalle_recurso['recurso']
                    
                    if nombre_recurso not in analisis_recursos:
                        analisis_recursos[nombre_recurso] = {
                            'recurso': nombre_recurso,
                            'ingresos': 0.0,
                            'horas_totales': 0.0,
                            'cantidad_total_usada': 0.0
                        }
                    
                    analisis_recursos[nombre_recurso]['ingresos'] += detalle_recurso['costo']
                    analisis_recursos[nombre_recurso]['horas_totales'] += detalle_recurso['horas']
                    analisis_recursos[nombre_recurso]['cantidad_total_usada'] += detalle_recurso['cantidad']
        
        # Ordenar por ingresos
        resultado = sorted(
            analisis_recursos.values(),
            key=lambda x: x['ingresos'],
            reverse=True
        )
        
        # Redondear valores
        for item in resultado:
            item['ingresos'] = round(item['ingresos'], 2)
            item['horas_totales'] = round(item['horas_totales'], 2)
            item['cantidad_total_usada'] = round(item['cantidad_total_usada'], 2)
        
        return resultado
    
    def obtener_consumos_pendientes(self, nit_cliente=None):
        """
        Obtiene los consumos pendientes de facturar.
        
        Args:
            nit_cliente (str, optional): NIT del cliente
            
        Returns:
            dict: Diccionario con información de consumos pendientes
        """
        clientes = self.xml_manager.obtener_clientes()
        
        if nit_cliente:
            cliente_especifico = self.xml_manager.obtener_cliente_por_nit(nit_cliente)
            if cliente_especifico:
                clientes = [cliente_especifico]
            else:
                return {'error': f'Cliente con NIT {nit_cliente} no encontrado'}
        
        resultado = []
        
        for cliente in clientes:
            info_cliente = {
                'nit': cliente.nit,
                'nombre': cliente.nombre,
                'instancias': []
            }
            
            total_pendiente_cliente = 0.0
            
            for instancia in cliente.instancias:
                consumos_pendientes = [c for c in instancia.consumos if not c.facturado]
                
                if consumos_pendientes:
                    horas_pendientes = sum(c.tiempo for c in consumos_pendientes)
                    
                    # Calcular monto pendiente
                    configuracion = self.xml_manager.obtener_configuracion_por_id(instancia.id_configuracion)
                    recursos_dict = {r.id: r for r in self.xml_manager.obtener_recursos()}
                    
                    monto_pendiente = 0.0
                    if configuracion:
                        for id_recurso, cantidad in configuracion.recursos_config.items():
                            if id_recurso in recursos_dict:
                                recurso = recursos_dict[id_recurso]
                                monto_pendiente += recurso.calcular_costo(horas_pendientes, cantidad)
                    
                    info_cliente['instancias'].append({
                        'id_instancia': instancia.id,
                        'nombre_instancia': instancia.nombre,
                        'consumos_pendientes': len(consumos_pendientes),
                        'horas_pendientes': round(horas_pendientes, 2),
                        'monto_pendiente': round(monto_pendiente, 2)
                    })
                    
                    total_pendiente_cliente += monto_pendiente
            
            if info_cliente['instancias']:
                info_cliente['total_pendiente'] = round(total_pendiente_cliente, 2)
                resultado.append(info_cliente)
        
        return resultado
    
    def obtener_resumen_facturacion(self):
        """
        Obtiene un resumen general de la facturación.
        
        Returns:
            dict: Resumen con estadísticas
        """
        facturas = self.xml_manager.obtener_facturas()
        
        if not facturas:
            return {
                'total_facturas': 0,
                'ingresos_totales': 0.0,
                'factura_promedio': 0.0,
                'clientes_facturados': 0
            }
        
        ingresos_totales = sum(f.monto_total for f in facturas)
        clientes_unicos = len(set(f.nit_cliente for f in facturas))
        
        return {
            'total_facturas': len(facturas),
            'ingresos_totales': round(ingresos_totales, 2),
            'factura_promedio': round(ingresos_totales / len(facturas), 2),
            'clientes_facturados': clientes_unicos,
            'factura_minima': round(min(f.monto_total for f in facturas), 2),
            'factura_maxima': round(max(f.monto_total for f in facturas), 2)
        }
import xml.etree.ElementTree as ET
from datetime import datetime

class DetalleFactura:
    """Representa el detalle de una factura por instancia."""
    
    def __init__(self, id_instancia, nombre_instancia, horas_consumidas, costo_total):
        self._id_instancia = int(id_instancia)
        self._nombre_instancia = nombre_instancia
        self._horas_consumidas = float(horas_consumidas)
        self._costo_total = float(costo_total)
        self._detalles_recursos = []  # Lista de {recurso, cantidad, horas, costo}
    
    @property
    def id_instancia(self):
        return self._id_instancia
    
    @property
    def nombre_instancia(self):
        return self._nombre_instancia
    
    @property
    def horas_consumidas(self):
        return self._horas_consumidas
    
    @property
    def costo_total(self):
        return self._costo_total
    
    @property
    def detalles_recursos(self):
        return self._detalles_recursos
    
    def agregar_detalle_recurso(self, recurso_nombre, cantidad, horas, costo):
        self._detalles_recursos.append({
            'recurso': recurso_nombre,
            'cantidad': cantidad,
            'horas': horas,
            'costo': costo
        })
    
    def to_dict(self):
        return {
            'id_instancia': self._id_instancia,
            'nombre_instancia': self._nombre_instancia,
            'horas_consumidas': self._horas_consumidas,
            'costo_total': self._costo_total,
            'detalles_recursos': self._detalles_recursos
        }


class Factura:
    """Representa una factura generada para un cliente."""
    
    def __init__(self, numero, nit_cliente, fecha, monto_total=0.0):
        self._numero = int(numero)
        self._nit_cliente = nit_cliente
        self._fecha = fecha
        self._monto_total = float(monto_total)
        self._detalles = []  # Lista de DetalleFactura
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def nit_cliente(self):
        return self._nit_cliente
    
    @property
    def fecha(self):
        return self._fecha
    
    @property
    def monto_total(self):
        return self._monto_total
    
    @property
    def detalles(self):
        return self._detalles
    
    def agregar_detalle(self, detalle):
        """Agrega un detalle a la factura."""
        self._detalles.append(detalle)
        self._monto_total += detalle.costo_total
    
    def to_dict(self, incluir_detalles=True):
        data = {
            'numero': self._numero,
            'nit_cliente': self._nit_cliente,
            'fecha': self._fecha,
            'monto_total': round(self._monto_total, 2)
        }
        
        if incluir_detalles:
            data['detalles'] = [d.to_dict() for d in self._detalles]
        
        return data
    
    def to_xml_element(self):
        factura_elem = ET.Element('factura', numero=str(self._numero))
        ET.SubElement(factura_elem, 'nitCliente').text = self._nit_cliente
        ET.SubElement(factura_elem, 'fecha').text = self._fecha
        ET.SubElement(factura_elem, 'montoTotal').text = str(round(self._monto_total, 2))
        
        detalles_elem = ET.SubElement(factura_elem, 'detalles')
        for detalle in self._detalles:
            det_elem = ET.SubElement(detalles_elem, 'detalle')
            ET.SubElement(det_elem, 'idInstancia').text = str(detalle.id_instancia)
            ET.SubElement(det_elem, 'nombreInstancia').text = detalle.nombre_instancia
            ET.SubElement(det_elem, 'horasConsumidas').text = str(detalle.horas_consumidas)
            ET.SubElement(det_elem, 'costoTotal').text = str(round(detalle.costo_total, 2))
            
            recursos_elem = ET.SubElement(det_elem, 'recursos')
            for rec in detalle.detalles_recursos:
                rec_elem = ET.SubElement(recursos_elem, 'recurso')
                ET.SubElement(rec_elem, 'nombre').text = rec['recurso']
                ET.SubElement(rec_elem, 'cantidad').text = str(rec['cantidad'])
                ET.SubElement(rec_elem, 'horas').text = str(rec['horas'])
                ET.SubElement(rec_elem, 'costo').text = str(round(rec['costo'], 2))
        
        return factura_elem
    
    @staticmethod
    def from_xml_element(element):
        numero = element.get('numero')
        nit_cliente = element.find('nitCliente').text
        fecha = element.find('fecha').text
        monto_total = element.find('montoTotal').text
        
        factura = Factura(numero, nit_cliente, fecha, monto_total)
        
        # Cargar detalles si existen
        detalles_elem = element.find('detalles')
        if detalles_elem is not None:
            for det_elem in detalles_elem.findall('detalle'):
                id_inst = det_elem.find('idInstancia').text
                nombre_inst = det_elem.find('nombreInstancia').text
                horas = det_elem.find('horasConsumidas').text
                costo = det_elem.find('costoTotal').text
                
                detalle = DetalleFactura(id_inst, nombre_inst, horas, costo)
                
                # Cargar recursos del detalle
                recursos_elem = det_elem.find('recursos')
                if recursos_elem is not None:
                    for rec_elem in recursos_elem.findall('recurso'):
                        detalle.agregar_detalle_recurso(
                            recurso_nombre=rec_elem.find('nombre').text,
                            cantidad=float(rec_elem.find('cantidad').text),
                            horas=float(rec_elem.find('horas').text),
                            costo=float(rec_elem.find('costo').text)
                        )
                
                factura._detalles.append(detalle)
        
        return factura
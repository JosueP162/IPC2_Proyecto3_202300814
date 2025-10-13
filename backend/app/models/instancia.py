import xml.etree.ElementTree as ET
from datetime import datetime

class Instancia:
    """Representa una instancia aprovisionada por un cliente."""
    
    def __init__(self, id, id_configuracion, nombre, fecha_inicio, estado, fecha_final=None):
        self._id = int(id)
        self._id_configuracion = int(id_configuracion)
        self._nombre = nombre.strip()
        self._fecha_inicio = fecha_inicio
        self._estado = estado.strip()
        self._fecha_final = fecha_final
        self._consumos = []
        
        if self._estado not in ['Vigente', 'Cancelada']:
            raise ValueError(f"Estado inválido: {self._estado}")
    
    @property
    def id(self):
        return self._id
    
    @property
    def id_configuracion(self):
        return self._id_configuracion
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def fecha_inicio(self):
        return self._fecha_inicio
    
    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, valor):
        if valor not in ['Vigente', 'Cancelada']:
            raise ValueError(f"Estado inválido: {valor}")
        self._estado = valor
    
    @property
    def fecha_final(self):
        return self._fecha_final
    
    @fecha_final.setter
    def fecha_final(self, valor):
        self._fecha_final = valor
    
    @property
    def consumos(self):
        return self._consumos
    
    def agregar_consumo(self, consumo):
        """Agrega un consumo a esta instancia."""
        self._consumos.append(consumo)
    
    def calcular_horas_totales(self, solo_no_facturados=False):
        """Calcula las horas totales de uso."""
        total = 0.0
        for consumo in self._consumos:
            if solo_no_facturados and consumo.facturado:
                continue
            total += consumo.tiempo
        return total
    
    def to_dict(self, incluir_consumos=False):
        data = {
            'id': self._id,
            'id_configuracion': self._id_configuracion,
            'nombre': self._nombre,
            'fecha_inicio': self._fecha_inicio,
            'estado': self._estado,
            'fecha_final': self._fecha_final
        }
        
        if incluir_consumos:
            data['consumos'] = [c.to_dict() for c in self._consumos]
        
        return data
    
    @staticmethod
    def from_xml_element(element, utils):
        """
        Crea una Instancia desde XML.
        
        Args:
            element: Elemento XML
            utils: Módulo de utilidades con extraer_fecha
        """
        fecha_inicio_text = element.find('fechaInicio').text
        fecha_inicio = utils.extraer_fecha(fecha_inicio_text)
        
        fecha_final = None
        fecha_final_elem = element.find('fechaFinal')
        if fecha_final_elem is not None and fecha_final_elem.text:
            fecha_final = utils.extraer_fecha(fecha_final_elem.text)
        
        return Instancia(
            id=element.get('id'),
            id_configuracion=element.find('idConfiguracion').text,
            nombre=element.find('nombre').text,
            fecha_inicio=fecha_inicio,
            estado=element.find('estado').text,
            fecha_final=fecha_final
        )
    
    def to_xml_element(self):
        inst_elem = ET.Element('instancia', id=str(self._id))
        ET.SubElement(inst_elem, 'idConfiguracion').text = str(self._id_configuracion)
        ET.SubElement(inst_elem, 'nombre').text = self._nombre
        ET.SubElement(inst_elem, 'fechaInicio').text = self._fecha_inicio or ''
        ET.SubElement(inst_elem, 'estado').text = self._estado
        ET.SubElement(inst_elem, 'fechaFinal').text = self._fecha_final or ''
        return inst_elem
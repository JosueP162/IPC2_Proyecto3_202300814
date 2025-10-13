import xml.etree.ElementTree as ET

class Consumo:
    """Representa un consumo de recursos de una instancia."""
    
    def __init__(self, tiempo, fecha_hora, facturado=False):
        self._tiempo = float(tiempo)
        self._fecha_hora = fecha_hora
        self._facturado = facturado
    
    @property
    def tiempo(self):
        return self._tiempo
    
    @property
    def fecha_hora(self):
        return self._fecha_hora
    
    @property
    def facturado(self):
        return self._facturado
    
    @facturado.setter
    def facturado(self, valor):
        self._facturado = valor
    
    def to_dict(self):
        return {
            'tiempo': self._tiempo,
            'fecha_hora': self._fecha_hora,
            'facturado': self._facturado
        }
    
    @staticmethod
    def from_xml_element(element, utils):
        tiempo = element.find('tiempo').text
        fecha_hora_text = element.find('fechaHora').text
        fecha_hora = utils.extraer_fecha_hora(fecha_hora_text)
        
        return Consumo(
            tiempo=tiempo,
            fecha_hora=fecha_hora
        )
    
    def to_xml_element(self):
        consumo_elem = ET.Element('consumo')
        ET.SubElement(consumo_elem, 'tiempo').text = str(self._tiempo)
        ET.SubElement(consumo_elem, 'fechaHora').text = self._fecha_hora or ''
        ET.SubElement(consumo_elem, 'facturado').text = str(self._facturado)
        return consumo_elem
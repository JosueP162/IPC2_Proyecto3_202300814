import xml.etree.ElementTree as ET

class Recurso:
    """Representa un recurso de infraestructura (Hardware o Software)."""
    
    def __init__(self, id, nombre, abreviatura, metrica, tipo, valor_x_hora):
        self._id = int(id)
        self._nombre = nombre.strip()
        self._abreviatura = abreviatura.strip()
        self._metrica = metrica.strip()
        self._tipo = tipo.strip()
        self._valor_x_hora = float(valor_x_hora)
        
        if self._tipo not in ['Hardware', 'Software']:
            raise ValueError(f"Tipo inválido: {self._tipo}")
    
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def abreviatura(self):
        return self._abreviatura
    
    @property
    def metrica(self):
        return self._metrica
    
    @property
    def tipo(self):
        return self._tipo
    
    @property
    def valor_x_hora(self):
        return self._valor_x_hora
    
    def calcular_costo(self, horas, cantidad=1):
        """Calcula el costo por usar este recurso."""
        return self._valor_x_hora * horas * cantidad
    
    def to_dict(self):
        """Convierte a diccionario para JSON."""
        return {
            'id': self._id,
            'nombre': self._nombre,
            'abreviatura': self._abreviatura,
            'metrica': self._metrica,
            'tipo': self._tipo,
            'valor_x_hora': self._valor_x_hora
        }
    
    @staticmethod
    def from_xml_element(element):
        """Crea un Recurso desde un elemento XML."""
        return Recurso(
            id=element.get('id'),
            nombre=element.find('nombre').text,
            abreviatura=element.find('abreviatura').text,
            metrica=element.find('metrica').text,
            tipo=element.find('tipo').text,
            valor_x_hora=element.find('valorXhora').text
        )
    
    def to_xml_element(self):
        """Convierte a elemento XML."""
        recurso_elem = ET.Element('recurso', id=str(self._id))
        ET.SubElement(recurso_elem, 'nombre').text = self._nombre
        ET.SubElement(recurso_elem, 'abreviatura').text = self._abreviatura
        ET.SubElement(recurso_elem, 'metrica').text = self._metrica
        ET.SubElement(recurso_elem, 'tipo').text = self._tipo
        ET.SubElement(recurso_elem, 'valorXhora').text = str(self._valor_x_hora)
        return recurso_elem
    
    def __str__(self):
        return f"Recurso({self._id}, {self._nombre}, ${self._valor_x_hora}/h)"
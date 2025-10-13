import xml.etree.ElementTree as ET

class Configuracion:
    """Representa una configuración de infraestructura."""
    
    def __init__(self, id, nombre, descripcion, recursos_config=None):
        self._id = int(id)
        self._nombre = nombre.strip()
        self._descripcion = descripcion.strip()
        self._recursos_config = recursos_config or {}  # {idRecurso: cantidad}
    
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def descripcion(self):
        return self._descripcion
    
    @property
    def recursos_config(self):
        return self._recursos_config
    
    def agregar_recurso(self, id_recurso, cantidad):
        """Agrega un recurso a la configuración."""
        self._recursos_config[int(id_recurso)] = float(cantidad)
    
    def calcular_costo_por_hora(self, recursos_disponibles):
        """
        Calcula el costo por hora de esta configuración.
        
        Args:
            recursos_disponibles (dict): {id: Recurso}
        """
        costo_total = 0.0
        for id_recurso, cantidad in self._recursos_config.items():
            if id_recurso in recursos_disponibles:
                recurso = recursos_disponibles[id_recurso]
                costo_total += recurso.calcular_costo(1, cantidad)
        return costo_total
    
    def to_dict(self):
        return {
            'id': self._id,
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'recursos': self._recursos_config
        }
    
    @staticmethod
    def from_xml_element(element):
        config = Configuracion(
            id=element.get('id'),
            nombre=element.find('nombre').text,
            descripcion=element.find('descripcion').text
        )
        
        recursos_elem = element.find('recursosConfiguracion')
        if recursos_elem is not None:
            for recurso_elem in recursos_elem.findall('recurso'):
                id_recurso = recurso_elem.get('id')
                cantidad = recurso_elem.text
                config.agregar_recurso(id_recurso, cantidad)
        
        return config
    
    def to_xml_element(self):
        config_elem = ET.Element('configuracion', id=str(self._id))
        ET.SubElement(config_elem, 'nombre').text = self._nombre
        ET.SubElement(config_elem, 'descripcion').text = self._descripcion
        
        recursos_elem = ET.SubElement(config_elem, 'recursosConfiguracion')
        for id_recurso, cantidad in self._recursos_config.items():
            rec_elem = ET.SubElement(recursos_elem, 'recurso', id=str(id_recurso))
            rec_elem.text = str(cantidad)
        
        return config_elem
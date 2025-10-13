import xml.etree.ElementTree as ET
from .configuracion import Configuracion

class Categoria:
    """Representa una categoría de configuraciones."""
    
    def __init__(self, id, nombre, descripcion, carga_trabajo):
        self._id = int(id)
        self._nombre = nombre.strip()
        self._descripcion = descripcion.strip()
        self._carga_trabajo = carga_trabajo.strip()
        self._configuraciones = []
    
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
    def carga_trabajo(self):
        return self._carga_trabajo
    
    @property
    def configuraciones(self):
        return self._configuraciones
    
    def agregar_configuracion(self, configuracion):
        """Agrega una configuración a la categoría."""
        self._configuraciones.append(configuracion)
    
    def to_dict(self, incluir_configuraciones=True):
        data = {
            'id': self._id,
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'carga_trabajo': self._carga_trabajo
        }
        
        if incluir_configuraciones:
            data['configuraciones'] = [c.to_dict() for c in self._configuraciones]
        
        return data
    
    @staticmethod
    def from_xml_element(element):
        categoria = Categoria(
            id=element.get('id'),
            nombre=element.find('nombre').text,
            descripcion=element.find('descripcion').text,
            carga_trabajo=element.find('cargaTrabajo').text
        )
        
        configs_elem = element.find('listaConfiguraciones')
        if configs_elem is not None:
            for config_elem in configs_elem.findall('configuracion'):
                config = Configuracion.from_xml_element(config_elem)
                categoria.agregar_configuracion(config)
        
        return categoria
    
    def to_xml_element(self):
        cat_elem = ET.Element('categoria', id=str(self._id))
        ET.SubElement(cat_elem, 'nombre').text = self._nombre
        ET.SubElement(cat_elem, 'descripcion').text = self._descripcion
        ET.SubElement(cat_elem, 'cargaTrabajo').text = self._carga_trabajo
        
        configs_elem = ET.SubElement(cat_elem, 'listaConfiguraciones')
        for config in self._configuraciones:
            configs_elem.append(config.to_xml_element())
        
        return cat_elem
    
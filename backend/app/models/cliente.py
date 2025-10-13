import xml.etree.ElementTree as ET
from .instancia import Instancia

class Cliente:
    """Representa un cliente de Tecnologías Chapinas."""
    
    def __init__(self, nit, nombre, usuario, clave, direccion, correo_electronico):
        self._nit = nit.strip()
        self._nombre = nombre.strip()
        self._usuario = usuario.strip()
        self._clave = clave.strip()
        self._direccion = direccion.strip()
        self._correo_electronico = correo_electronico.strip()
        self._instancias = []
    
    @property
    def nit(self):
        return self._nit
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def usuario(self):
        return self._usuario
    
    @property
    def direccion(self):
        return self._direccion
    
    @property
    def correo_electronico(self):
        return self._correo_electronico
    
    @property
    def instancias(self):
        return self._instancias
    
    def agregar_instancia(self, instancia):
        """Agrega una instancia al cliente."""
        self._instancias.append(instancia)
    
    def obtener_instancia_por_id(self, id_instancia):
        """Busca una instancia por su ID."""
        for instancia in self._instancias:
            if instancia.id == id_instancia:
                return instancia
        return None
    
    def to_dict(self, incluir_instancias=True):
        data = {
            'nit': self._nit,
            'nombre': self._nombre,
            'usuario': self._usuario,
            'direccion': self._direccion,
            'correo_electronico': self._correo_electronico
        }
        
        if incluir_instancias:
            data['instancias'] = [i.to_dict() for i in self._instancias]
        
        return data
    
    @staticmethod
    def from_xml_element(element, utils):
        cliente = Cliente(
            nit=element.get('nit'),
            nombre=element.find('nombre').text,
            usuario=element.find('usuario').text,
            clave=element.find('clave').text,
            direccion=element.find('direccion').text,
            correo_electronico=element.find('correoElectronico').text
        )
        
        instancias_elem = element.find('listaInstancias')
        if instancias_elem is not None:
            for inst_elem in instancias_elem.findall('instancia'):
                instancia = Instancia.from_xml_element(inst_elem, utils)
                cliente.agregar_instancia(instancia)
        
        return cliente
    
    def to_xml_element(self):
        cliente_elem = ET.Element('cliente', nit=self._nit)
        ET.SubElement(cliente_elem, 'nombre').text = self._nombre
        ET.SubElement(cliente_elem, 'usuario').text = self._usuario
        ET.SubElement(cliente_elem, 'clave').text = self._clave
        ET.SubElement(cliente_elem, 'direccion').text = self._direccion
        ET.SubElement(cliente_elem, 'correoElectronico').text = self._correo_electronico
        
        instancias_elem = ET.SubElement(cliente_elem, 'listaInstancias')
        for instancia in self._instancias:
            instancias_elem.append(instancia.to_xml_element())
        
        return cliente_elem
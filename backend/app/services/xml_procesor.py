import xml.etree.ElementTree as ET
from app.models import Recurso, Categoria, Cliente, Consumo
from app.utils import regex_utils

class XMLConfigProcessor:
    """Procesa el XML de configuración de entrada."""
    
    def __init__(self, xml_string):
        self.root = ET.fromstring(xml_string)
        self.recursos = []
        self.categorias = []
        self.clientes = []
    
    def procesar(self):
        """Procesa todo el XML y extrae todos los objetos."""
        self._procesar_recursos()
        self._procesar_categorias()
        self._procesar_clientes()
        
        return {
            'recursos_procesados': len(self.recursos),
            'categorias_procesadas': len(self.categorias),
            'clientes_procesados': len(self.clientes),
            'instancias_procesadas': sum(len(c.instancias) for c in self.clientes),
            'configuraciones_procesadas': sum(len(cat.configuraciones) for cat in self.categorias)
        }
    
    def _procesar_recursos(self):
        """Procesa todos los recursos del XML."""
        lista_recursos = self.root.find('listaRecursos')
        
        if lista_recursos is not None:
            for recurso_elem in lista_recursos.findall('recurso'):
                try:
                    recurso = Recurso.from_xml_element(recurso_elem)
                    self.recursos.append(recurso)
                except Exception as e:
                    print(f"Error procesando recurso: {e}")
    
    def _procesar_categorias(self):
        """Procesa todas las categorías del XML."""
        lista_categorias = self.root.find('listaCategorias')
        
        if lista_categorias is not None:
            for categoria_elem in lista_categorias.findall('categoria'):
                try:
                    categoria = Categoria.from_xml_element(categoria_elem)
                    self.categorias.append(categoria)
                except Exception as e:
                    print(f"Error procesando categoría: {e}")
    
    def _procesar_clientes(self):
        """Procesa todos los clientes del XML."""
        lista_clientes = self.root.find('listaClientes')
        
        if lista_clientes is not None:
            for cliente_elem in lista_clientes.findall('cliente'):
                try:
                    nit = cliente_elem.get('nit')
                    if not regex_utils.validar_nit(nit):
                        print(f"NIT inválido: {nit}")
                        continue
                    
                    cliente = Cliente.from_xml_element(cliente_elem, regex_utils)
                    self.clientes.append(cliente)
                except Exception as e:
                    print(f"Error procesando cliente: {e}")


class XMLConsumoProcessor:
    """Procesa el XML de consumos de entrada."""
    
    def __init__(self, xml_string):
        self.root = ET.fromstring(xml_string)
        self.consumos = []  # Lista de tuplas (nit, id_instancia, consumo)
    
    def procesar(self):
        """Procesa todos los consumos del XML."""
        for consumo_elem in self.root.findall('consumo'):
            try:
                nit_cliente = consumo_elem.get('nitCliente')
                id_instancia = int(consumo_elem.get('idInstancia'))
                
                if not regex_utils.validar_nit(nit_cliente):
                    print(f"NIT inválido en consumo: {nit_cliente}")
                    continue
                
                consumo = Consumo.from_xml_element(consumo_elem, regex_utils)
                self.consumos.append((nit_cliente, id_instancia, consumo))
                
            except Exception as e:
                print(f"Error procesando consumo: {e}")
        
        return {
            'consumos_procesados': len(self.consumos)
        }
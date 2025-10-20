import xml.etree.ElementTree as ET
import os
from app.models import Recurso, Categoria, Cliente, Factura

class XMLManager:
    """Maneja la persistencia en XML (base de datos)."""
    
    def __init__(self, archivo='app/database/data.xml'):
        self.archivo = archivo
        self._init_database()
    
    def _init_database(self):
        """Crea el archivo XML si no existe."""
        if not os.path.exists(self.archivo):
            os.makedirs(os.path.dirname(self.archivo), exist_ok=True)
            root = ET.Element('database')
            ET.SubElement(root, 'recursos')
            ET.SubElement(root, 'categorias')
            ET.SubElement(root, 'clientes')
            ET.SubElement(root, 'facturas')
            
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ")
            tree.write(self.archivo, encoding='utf-8', xml_declaration=True)
    
    def limpiar_database(self):
        """Elimina todos los datos (Inicializar Sistema)."""
        if os.path.exists(self.archivo):
            os.remove(self.archivo)
        self._init_database()
    
    # ==================== RECURSOS ====================
    
    def guardar_recurso(self, recurso):
        """Guarda un recurso en el XML."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        recursos_node = root.find('recursos')
        
        # Verificar si ya existe
        for rec_elem in recursos_node.findall('recurso'):
            if int(rec_elem.get('id')) == recurso.id:
                recursos_node.remove(rec_elem)
                break
        
        recursos_node.append(recurso.to_xml_element())
        
        ET.indent(tree, space="  ")
        tree.write(self.archivo, encoding='utf-8', xml_declaration=True)
    
    def obtener_recursos(self):
        """Obtiene todos los recursos del XML."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        recursos = []
        recursos_node = root.find('recursos')
        
        for recurso_elem in recursos_node.findall('recurso'):
            recurso = Recurso.from_xml_element(recurso_elem)
            recursos.append(recurso)
        
        return recursos
    
    def obtener_recurso_por_id(self, id_recurso):
        """Obtiene un recurso por su ID."""
        recursos = self.obtener_recursos()
        for recurso in recursos:
            if recurso.id == int(id_recurso):
                return recurso
        return None
    
    def eliminar_recurso(self, id_recurso):
        """Elimina un recurso del XML."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        recursos_node = root.find('recursos')
        
        for rec_elem in recursos_node.findall('recurso'):
            if int(rec_elem.get('id')) == int(id_recurso):
                recursos_node.remove(rec_elem)
                ET.indent(tree, space="  ")
                tree.write(self.archivo, encoding='utf-8', xml_declaration=True)
                return True
        
        return False
    
    # ==================== CATEGORÍAS ====================
    
    def guardar_categoria(self, categoria):
        """Guarda una categoría con sus configuraciones."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        categorias_node = root.find('categorias')
        
        # Verificar si ya existe
        for cat_elem in categorias_node.findall('categoria'):
            if int(cat_elem.get('id')) == categoria.id:
                categorias_node.remove(cat_elem)
                break
        
        categorias_node.append(categoria.to_xml_element())
        
        ET.indent(tree, space="  ")
        tree.write(self.archivo, encoding='utf-8', xml_declaration=True)
    
    def obtener_categorias(self):
        """Obtiene todas las categorías con sus configuraciones."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        categorias = []
        categorias_node = root.find('categorias')
        
        for cat_elem in categorias_node.findall('categoria'):
            categoria = Categoria.from_xml_element(cat_elem)
            categorias.append(categoria)
        
        return categorias
    
    def obtener_categoria_por_id(self, id_categoria):
        """Obtiene una categoría por su ID."""
        categorias = self.obtener_categorias()
        for categoria in categorias:
            if categoria.id == int(id_categoria):
                return categoria
        return None
    
    def obtener_configuracion_por_id(self, id_configuracion):
        """Busca una configuración por ID en todas las categorías."""
        categorias = self.obtener_categorias()
        for categoria in categorias:
            for config in categoria.configuraciones:
                if config.id == int(id_configuracion):
                    return config
        return None
    
    def eliminar_categoria(self, id_categoria):
        """Elimina una categoría del XML."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        categorias_node = root.find('categorias')
        
        for cat_elem in categorias_node.findall('categoria'):
            if int(cat_elem.get('id')) == int(id_categoria):
                categorias_node.remove(cat_elem)
                ET.indent(tree, space="  ")
                tree.write(self.archivo, encoding='utf-8', xml_declaration=True)
                return True
        
        return False
    
    # ==================== CLIENTES ====================
    
    def guardar_cliente(self, cliente):
        """Guarda un cliente con sus instancias."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        clientes_node = root.find('clientes')
        
        # Verificar si ya existe
        for cli_elem in clientes_node.findall('cliente'):
            if cli_elem.get('nit') == cliente.nit:
                clientes_node.remove(cli_elem)
                break
        
        clientes_node.append(cliente.to_xml_element())
        
        ET.indent(tree, space="  ")
        tree.write(self.archivo, encoding='utf-8', xml_declaration=True)
    
    def obtener_clientes(self):
        """Obtiene todos los clientes con sus instancias."""
        import app.utils.regex_utils as utils
        
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        clientes = []
        clientes_node = root.find('clientes')
        
        for cli_elem in clientes_node.findall('cliente'):
            cliente = Cliente.from_xml_element(cli_elem, utils)
            clientes.append(cliente)
        
        return clientes
    
    def obtener_cliente_por_nit(self, nit):
        """Obtiene un cliente por su NIT."""
        clientes = self.obtener_clientes()
        for cliente in clientes:
            if cliente.nit == nit:
                return cliente
        return None
    
    def eliminar_cliente(self, nit):
        """Elimina un cliente del XML."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        clientes_node = root.find('clientes')
        
        for cli_elem in clientes_node.findall('cliente'):
            if cli_elem.get('nit') == nit:
                clientes_node.remove(cli_elem)
                ET.indent(tree, space="  ")
                tree.write(self.archivo, encoding='utf-8', xml_declaration=True)
                return True
        
        return False
    
    # ==================== FACTURAS ====================
    
    def guardar_factura(self, factura):
        """Guarda una factura."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        facturas_node = root.find('facturas')
        facturas_node.append(factura.to_xml_element())
        
        ET.indent(tree, space="  ")
        tree.write(self.archivo, encoding='utf-8', xml_declaration=True)
    
    def obtener_facturas(self):
        """Obtiene todas las facturas."""
        tree = ET.parse(self.archivo)
        root = tree.getroot()
        
        facturas = []
        facturas_node = root.find('facturas')
        
        for fac_elem in facturas_node.findall('factura'):
            factura = Factura.from_xml_element(fac_elem)
            facturas.append(factura)
        
        return facturas
    
    def obtener_factura_por_numero(self, numero):
        """Obtiene una factura por su número."""
        facturas = self.obtener_facturas()
        for factura in facturas:
            if factura.numero == int(numero):
                return factura
        return None
    
    def obtener_facturas_por_cliente(self, nit_cliente):
        """Obtiene todas las facturas de un cliente."""
        facturas = self.obtener_facturas()
        return [f for f in facturas if f.nit_cliente == nit_cliente]
    
    def obtener_siguiente_numero_factura(self):
        """Obtiene el siguiente número de factura disponible."""
        facturas = self.obtener_facturas()
        if not facturas:
            return 1
        return max(f.numero for f in facturas) + 1
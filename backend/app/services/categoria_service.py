from app.database.xml_manager import XMLManager
from app.models import Categoria, Configuracion

class CategoriaService:
    """Servicio para gestionar categorías y configuraciones."""
    
    def __init__(self, xml_manager=None):
        self.xml_manager = xml_manager or XMLManager()
    
    def crear_categoria(self, datos):
        """
        Crea una nueva categoría.
        
        Args:
            datos (dict): Diccionario con id, nombre, descripcion, carga_trabajo
            
        Returns:
            Categoria: Categoría creada
            
        Raises:
            ValueError: Si falta algún campo requerido
        """
        # Validar que no exista ya
        categoria_existente = self.obtener_por_id(datos['id'])
        if categoria_existente:
            raise ValueError(f"Ya existe una categoría con ID {datos['id']}")
        
        categoria = Categoria(
            id=datos['id'],
            nombre=datos['nombre'],
            descripcion=datos['descripcion'],
            carga_trabajo=datos['carga_trabajo']
        )
        
        self.xml_manager.guardar_categoria(categoria)
        return categoria
    
    def obtener_todas(self, incluir_configuraciones=True):
        """
        Obtiene todas las categorías.
        
        Args:
            incluir_configuraciones (bool): Si incluir las configuraciones
            
        Returns:
            list: Lista de categorías
        """
        return self.xml_manager.obtener_categorias()
    
    def obtener_por_id(self, id_categoria):
        """
        Obtiene una categoría por su ID.
        
        Args:
            id_categoria (int): ID de la categoría
            
        Returns:
            Categoria: Categoría encontrada o None
        """
        return self.xml_manager.obtener_categoria_por_id(id_categoria)
    
    def actualizar_categoria(self, id_categoria, datos):
        """
        Actualiza una categoría existente.
        
        Args:
            id_categoria (int): ID de la categoría
            datos (dict): Datos a actualizar
            
        Returns:
            Categoria: Categoría actualizada
            
        Raises:
            ValueError: Si la categoría no existe
        """
        categoria_existente = self.obtener_por_id(id_categoria)
        if not categoria_existente:
            raise ValueError(f"Categoría con ID {id_categoria} no existe")
        
        # Crear nueva categoría con datos actualizados
        categoria_actualizada = Categoria(
            id=id_categoria,
            nombre=datos.get('nombre', categoria_existente.nombre),
            descripcion=datos.get('descripcion', categoria_existente.descripcion),
            carga_trabajo=datos.get('carga_trabajo', categoria_existente.carga_trabajo)
        )
        
        # Mantener las configuraciones existentes
        for config in categoria_existente.configuraciones:
            categoria_actualizada.agregar_configuracion(config)
        
        self.xml_manager.guardar_categoria(categoria_actualizada)
        return categoria_actualizada
    
    def agregar_configuracion(self, id_categoria, datos_config):
        """
        Agrega una configuración a una categoría.
        
        Args:
            id_categoria (int): ID de la categoría
            datos_config (dict): Datos de la configuración (id, nombre, descripcion, recursos)
            
        Returns:
            Configuracion: Configuración creada
            
        Raises:
            ValueError: Si la categoría no existe o la configuración ya existe
        """
        categoria = self.obtener_por_id(id_categoria)
        if not categoria:
            raise ValueError(f"Categoría con ID {id_categoria} no existe")
        
        # Verificar que no exista ya esta configuración
        for config in categoria.configuraciones:
            if config.id == int(datos_config['id']):
                raise ValueError(f"Ya existe una configuración con ID {datos_config['id']} en esta categoría")
        
        # Validar que los recursos existan
        if 'recursos' in datos_config and datos_config['recursos']:
            recursos_disponibles = self.xml_manager.obtener_recursos()
            ids_disponibles = {r.id for r in recursos_disponibles}
            
            for id_recurso in datos_config['recursos'].keys():
                if int(id_recurso) not in ids_disponibles:
                    raise ValueError(f"Recurso con ID {id_recurso} no existe")
        
        configuracion = Configuracion(
            id=datos_config['id'],
            nombre=datos_config['nombre'],
            descripcion=datos_config['descripcion'],
            recursos_config=datos_config.get('recursos', {})
        )
        
        categoria.agregar_configuracion(configuracion)
        self.xml_manager.guardar_categoria(categoria)
        
        return configuracion
    
    def actualizar_configuracion(self, id_configuracion, datos):
        """
        Actualiza una configuración existente.
        
        Args:
            id_configuracion (int): ID de la configuración
            datos (dict): Datos a actualizar
            
        Returns:
            Configuracion: Configuración actualizada
            
        Raises:
            ValueError: Si la configuración no existe
        """
        # Buscar la configuración y su categoría
        categorias = self.obtener_todas()
        categoria_encontrada = None
        config_encontrada = None
        
        for categoria in categorias:
            for config in categoria.configuraciones:
                if config.id == int(id_configuracion):
                    categoria_encontrada = categoria
                    config_encontrada = config
                    break
            if categoria_encontrada:
                break
        
        if not config_encontrada:
            raise ValueError(f"Configuración con ID {id_configuracion} no existe")
        
        # Validar recursos si se están actualizando
        if 'recursos' in datos and datos['recursos']:
            recursos_disponibles = self.xml_manager.obtener_recursos()
            ids_disponibles = {r.id for r in recursos_disponibles}
            
            for id_recurso in datos['recursos'].keys():
                if int(id_recurso) not in ids_disponibles:
                    raise ValueError(f"Recurso con ID {id_recurso} no existe")
        
        # Crear configuración actualizada
        config_actualizada = Configuracion(
            id=id_configuracion,
            nombre=datos.get('nombre', config_encontrada.nombre),
            descripcion=datos.get('descripcion', config_encontrada.descripcion),
            recursos_config=datos.get('recursos', config_encontrada.recursos_config)
        )
        
        # Reemplazar en la categoría
        categoria_encontrada._configuraciones = [
            config_actualizada if c.id == id_configuracion else c
            for c in categoria_encontrada.configuraciones
        ]
        
        self.xml_manager.guardar_categoria(categoria_encontrada)
        return config_actualizada
    
    def eliminar_configuracion(self, id_configuracion):
        """
        Elimina una configuración de su categoría.
        
        Args:
            id_configuracion (int): ID de la configuración
            
        Returns:
            bool: True si se eliminó, False si no existe
        """
        categorias = self.obtener_todas()
        
        for categoria in categorias:
            for config in categoria.configuraciones:
                if config.id == int(id_configuracion):
                    categoria._configuraciones.remove(config)
                    self.xml_manager.guardar_categoria(categoria)
                    return True
        
        return False
    
    def obtener_configuracion_por_id(self, id_configuracion):
        """
        Obtiene una configuración por su ID.
        
        Args:
            id_configuracion (int): ID de la configuración
            
        Returns:
            Configuracion: Configuración encontrada o None
        """
        return self.xml_manager.obtener_configuracion_por_id(id_configuracion)
    
    def eliminar_categoria(self, id_categoria):
        """
        Elimina una categoría completa.
        
        Args:
            id_categoria (int): ID de la categoría
            
        Returns:
            bool: True si se eliminó, False si no existe
            
        Raises:
            ValueError: Si hay instancias usando configuraciones de esta categoría
        """
        categoria = self.obtener_por_id(id_categoria)
        if not categoria:
            return False
        
        # Verificar que no haya instancias usando estas configuraciones
        clientes = self.xml_manager.obtener_clientes()
        ids_configs = {c.id for c in categoria.configuraciones}
        
        for cliente in clientes:
            for instancia in cliente.instancias:
                if instancia.id_configuracion in ids_configs:
                    raise ValueError(
                        f"No se puede eliminar: La configuración {instancia.id_configuracion} "
                        f"está siendo usada por la instancia {instancia.id} del cliente {cliente.nombre}"
                    )
        
        return self.xml_manager.eliminar_categoria(id_categoria)
    
    def obtener_configuraciones_con_costos(self):
        """
        Obtiene todas las configuraciones con su costo por hora calculado.
        
        Returns:
            list: Lista de diccionarios con configuración y costo
        """
        categorias = self.obtener_todas()
        recursos_dict = {r.id: r for r in self.xml_manager.obtener_recursos()}
        
        resultado = []
        
        for categoria in categorias:
            for config in categoria.configuraciones:
                costo_hora = config.calcular_costo_por_hora(recursos_dict)
                
                resultado.append({
                    'categoria_id': categoria.id,
                    'categoria_nombre': categoria.nombre,
                    'configuracion_id': config.id,
                    'configuracion_nombre': config.nombre,
                    'descripcion': config.descripcion,
                    'costo_por_hora': round(costo_hora, 2),
                    'recursos': config.recursos_config
                })
        
        return resultado
    
    def validar_configuracion(self, id_configuracion):
        """
        Valida que una configuración tenga todos sus recursos disponibles.
        
        Args:
            id_configuracion (int): ID de la configuración
            
        Returns:
            dict: Diccionario con resultado de validación
        """
        config = self.obtener_configuracion_por_id(id_configuracion)
        if not config:
            return {
                'valida': False,
                'mensaje': f'Configuración con ID {id_configuracion} no existe'
            }
        
        recursos_disponibles = {r.id for r in self.xml_manager.obtener_recursos()}
        recursos_faltantes = []
        
        for id_recurso in config.recursos_config.keys():
            if id_recurso not in recursos_disponibles:
                recursos_faltantes.append(id_recurso)
        
        if recursos_faltantes:
            return {
                'valida': False,
                'mensaje': 'Faltan recursos',
                'recursos_faltantes': recursos_faltantes
            }
        
        return {
            'valida': True,
            'mensaje': 'Configuración válida'
        }
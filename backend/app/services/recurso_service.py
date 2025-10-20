from app.database.xml_manager import XMLManager
from app.models import Recurso

class RecursoService:
    """Servicio para gestionar recursos."""
    
    def __init__(self, xml_manager=None):
        self.xml_manager = xml_manager or XMLManager()
    
    def crear_recurso(self, datos):
        """
        Crea un nuevo recurso.
        
        Args:
            datos (dict): Datos del recurso
            
        Returns:
            Recurso: Recurso creado
        """
        recurso = Recurso(
            id=datos['id'],
            nombre=datos['nombre'],
            abreviatura=datos['abreviatura'],
            metrica=datos['metrica'],
            tipo=datos['tipo'],
            valor_x_hora=datos['valor_x_hora']
        )
        
        self.xml_manager.guardar_recurso(recurso)
        return recurso
    
    def obtener_todos(self):
        """Obtiene todos los recursos."""
        return self.xml_manager.obtener_recursos()
    
    def obtener_por_id(self, id_recurso):
        """Obtiene un recurso por ID."""
        return self.xml_manager.obtener_recurso_por_id(id_recurso)
    
    def actualizar_recurso(self, id_recurso, datos):
        """Actualiza un recurso existente."""
        recurso_existente = self.obtener_por_id(id_recurso)
        if not recurso_existente:
            raise ValueError(f"Recurso con ID {id_recurso} no existe")
        
        recurso_actualizado = Recurso(
            id=id_recurso,
            nombre=datos.get('nombre', recurso_existente.nombre),
            abreviatura=datos.get('abreviatura', recurso_existente.abreviatura),
            metrica=datos.get('metrica', recurso_existente.metrica),
            tipo=datos.get('tipo', recurso_existente.tipo),
            valor_x_hora=datos.get('valor_x_hora', recurso_existente.valor_x_hora)
        )
        
        self.xml_manager.guardar_recurso(recurso_actualizado)
        return recurso_actualizado
    
    def eliminar_recurso(self, id_recurso):
        """Elimina un recurso."""
        return self.xml_manager.eliminar_recurso(id_recurso)
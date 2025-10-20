from app.database.xml_manager import XMLManager
from app.models import Cliente, Instancia
from app.utils.regex_utils import validar_nit

class ClienteService:
    """Servicio para gestionar clientes e instancias."""
    
    def __init__(self, xml_manager=None):
        self.xml_manager = xml_manager or XMLManager()
    
    def crear_cliente(self, datos):
        """Crea un nuevo cliente."""
        nit = datos['nit']
        if not validar_nit(nit):
            raise ValueError(f"NIT inválido: {nit}")
        
        cliente = Cliente(
            nit=nit,
            nombre=datos['nombre'],
            usuario=datos['usuario'],
            clave=datos['clave'],
            direccion=datos['direccion'],
            correo_electronico=datos['correo_electronico']
        )
        
        self.xml_manager.guardar_cliente(cliente)
        return cliente
    
    def obtener_todos(self):
        """Obtiene todos los clientes."""
        return self.xml_manager.obtener_clientes()
    
    def obtener_por_nit(self, nit):
        """Obtiene un cliente por NIT."""
        return self.xml_manager.obtener_cliente_por_nit(nit)
    
    def agregar_instancia(self, nit_cliente, datos_instancia):
        """Agrega una instancia a un cliente."""
        cliente = self.obtener_por_nit(nit_cliente)
        if not cliente:
            raise ValueError(f"Cliente con NIT {nit_cliente} no existe")
        
        # Verificar que la configuración existe
        config = self.xml_manager.obtener_configuracion_por_id(datos_instancia['id_configuracion'])
        if not config:
            raise ValueError(f"Configuración con ID {datos_instancia['id_configuracion']} no existe")
        
        instancia = Instancia(
            id=datos_instancia['id'],
            id_configuracion=datos_instancia['id_configuracion'],
            nombre=datos_instancia['nombre'],
            fecha_inicio=datos_instancia['fecha_inicio'],
            estado=datos_instancia['estado'],
            fecha_final=datos_instancia.get('fecha_final')
        )
        
        cliente.agregar_instancia(instancia)
        self.xml_manager.guardar_cliente(cliente)
        
        return instancia
    
    def cancelar_instancia(self, nit_cliente, id_instancia, fecha_final):
        """Cancela una instancia de un cliente."""
        cliente = self.obtener_por_nit(nit_cliente)
        if not cliente:
            raise ValueError(f"Cliente con NIT {nit_cliente} no existe")
        
        instancia = cliente.obtener_instancia_por_id(id_instancia)
        if not instancia:
            raise ValueError(f"Instancia con ID {id_instancia} no existe")
        
        instancia.estado = 'Cancelada'
        instancia.fecha_final = fecha_final
        
        self.xml_manager.guardar_cliente(cliente)
        return instancia
    
    def agregar_consumo(self, nit_cliente, id_instancia, consumo):
        """Agrega un consumo a una instancia."""
        cliente = self.obtener_por_nit(nit_cliente)
        if not cliente:
            raise ValueError(f"Cliente con NIT {nit_cliente} no existe")
        
        instancia = cliente.obtener_instancia_por_id(id_instancia)
        if not instancia:
            raise ValueError(f"Instancia con ID {id_instancia} no existe para el cliente {nit_cliente}")
        
        instancia.agregar_consumo(consumo)
        self.xml_manager.guardar_cliente(cliente)
        
        return True
    
    def eliminar_cliente(self, nit):
        """Elimina un cliente."""
        return self.xml_manager.eliminar_cliente(nit)
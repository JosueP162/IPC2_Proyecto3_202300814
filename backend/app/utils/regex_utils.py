import re
from datetime import datetime

def extraer_fecha(texto):
    """
    Extrae la primera fecha válida en formato dd/mm/yyyy.
    
    Args:
        texto (str): Texto que puede contener una fecha
        
    Returns:
        str: Fecha en formato dd/mm/yyyy o None
    """
    if not texto:
        return None
    
    patron = r'\b(\d{2})/(\d{2})/(\d{4})\b'
    match = re.search(patron, texto)
    
    if match:
        dia, mes, anio = match.groups()
        dia, mes, anio = int(dia), int(mes), int(anio)
        
        try:
            datetime(anio, mes, dia)
            return f"{dia:02d}/{mes:02d}/{anio}"
        except ValueError:
            return None
    
    return None


def extraer_fecha_hora(texto):
    """
    Extrae fecha y hora en formato dd/mm/yyyy hh:mm.
    
    Returns:
        str: Fecha-hora en formato dd/mm/yyyy hh:mm o None
    """
    if not texto:
        return None
    
    patron = r'\b(\d{2})/(\d{2})/(\d{4})\s+(\d{2}):(\d{2})\b'
    match = re.search(patron, texto)
    
    if match:
        dia, mes, anio, hora, minuto = match.groups()
        try:
            datetime(int(anio), int(mes), int(dia), int(hora), int(minuto))
            return f"{dia}/{mes}/{anio} {hora}:{minuto}"
        except ValueError:
            return None
    
    return None


def validar_nit(nit):
    """
    Valida formato de NIT guatemalteco.
    Formato: dígitos-[0-9K]
    
    Ejemplos válidos: 12345-6, 110339001-K
    """
    if not nit:
        return False
    
    patron = r'^\d+-[0-9K]$'
    return bool(re.match(patron, nit))
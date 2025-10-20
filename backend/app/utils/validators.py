from datetime import datetime

def validar_tipo_recurso(tipo):
    """Valida que el tipo de recurso sea Hardware o Software."""
    return tipo in ['Hardware', 'Software']


def validar_estado_instancia(estado):
    """Valida que el estado sea Vigente o Cancelada."""
    return estado in ['Vigente', 'Cancelada']


def validar_fecha(fecha_str):
    """Valida formato de fecha dd/mm/yyyy."""
    try:
        datetime.strptime(fecha_str, '%d/%m/%Y')
        return True
    except:
        return False


def validar_rango_fechas(fecha_inicio, fecha_fin):
    """Valida que fecha_inicio sea menor o igual a fecha_fin."""
    try:
        inicio = datetime.strptime(fecha_inicio, '%d/%m/%Y')
        fin = datetime.strptime(fecha_fin, '%d/%m/%Y')
        return inicio <= fin
    except:
        return False
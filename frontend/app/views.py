# [file name]: app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
import json
from .services import BackendService
from .pdf_generator import generar_pdf_factura, generar_pdf_analisis

def home(request):
    """Página principal - Dashboard"""
    estado = BackendService.obtener_estado_sistema()
    context = {
        'estado': estado.get('data', {}) if estado.get('success') else {}
    }
    return render(request, 'app/home.html', context)

# ==================== ENVIAR MENSAJES XML ====================

def configuracion_xml(request):
    """Enviar mensaje de configuración XML"""
    if request.method == 'POST' and request.FILES.get('archivo_xml'):
        archivo = request.FILES['archivo_xml']
        if not archivo.name.endswith('.xml'):
            messages.error(request, 'El archivo debe ser XML')
        else:
            resultado = BackendService.cargar_configuracion_xml(archivo)
            if resultado.get('success'):
                messages.success(request, resultado.get('message', 'Configuración cargada exitosamente'))
            else:
                messages.error(request, resultado.get('message', 'Error al cargar configuración'))
    
    return render(request, 'app/configuracion_xml.html')

def consumos_xml(request):
    """Enviar mensaje de consumos XML"""
    if request.method == 'POST' and request.FILES.get('archivo_xml'):
        archivo = request.FILES['archivo_xml']
        if not archivo.name.endswith('.xml'):
            messages.error(request, 'El archivo debe ser XML')
        else:
            resultado = BackendService.cargar_consumos_xml(archivo)
            if resultado.get('success'):
                messages.success(request, resultado.get('message', 'Consumos cargados exitosamente'))
            else:
                messages.error(request, resultado.get('message', 'Error al cargar consumos'))
    
    return render(request, 'app/consumos_xml.html')

# ==================== OPERACIONES DEL SISTEMA ====================

def inicializar_sistema(request):
    """Inicializar sistema (eliminar todos los datos)"""
    if request.method == 'POST':
        resultado = BackendService.inicializar_sistema()
        if resultado.get('success'):
            messages.success(request, 'Sistema inicializado exitosamente')
        else:
            messages.error(request, resultado.get('message', 'Error al inicializar sistema'))
        return redirect('home')
    
    return render(request, 'app/inicializar_sistema.html')

def consultar_datos(request):
    """Consultar todos los datos del sistema"""
    recursos = BackendService.obtener_recursos()
    categorias = BackendService.obtener_categorias()
    clientes = BackendService.obtener_clientes()
    estado = BackendService.obtener_estado_sistema()
    consumos_pendientes = BackendService.obtener_consumos_pendientes()
    
    context = {
        'recursos': recursos.get('data', []) if recursos.get('success') else [],
        'categorias': categorias.get('data', []) if categorias.get('success') else [],
        'clientes': clientes.get('data', []) if clientes.get('success') else [],
        'estado': estado.get('data', {}) if estado.get('success') else {},
        'consumos_pendientes': consumos_pendientes.get('data', []) if consumos_pendientes.get('success') else [],
    }
    return render(request, 'app/consultar_datos.html', context)

# ==================== CREACIÓN DE DATOS ====================

def crear_recurso(request):
    """Crear nuevo recurso"""
    if request.method == 'POST':
        datos = {
            'id': int(request.POST['id']),
            'nombre': request.POST['nombre'],
            'abreviatura': request.POST['abreviatura'],
            'metrica': request.POST['metrica'],
            'tipo': request.POST['tipo'],
            'valor_x_hora': float(request.POST['valor_x_hora'])
        }
        resultado = BackendService.crear_recurso(datos)
        if resultado.get('success'):
            messages.success(request, 'Recurso creado exitosamente')
            return redirect('consultar_datos')
        else:
            messages.error(request, resultado.get('message', 'Error al crear recurso'))
    
    return render(request, 'app/crear_recurso.html')

def crear_categoria(request):
    """Crear nueva categoría"""
    if request.method == 'POST':
        datos = {
            'id': int(request.POST['id']),
            'nombre': request.POST['nombre'],
            'descripcion': request.POST['descripcion'],
            'carga_trabajo': request.POST['carga_trabajo']
        }
        resultado = BackendService.crear_categoria(datos)
        if resultado.get('success'):
            messages.success(request, 'Categoría creada exitosamente')
            return redirect('consultar_datos')
        else:
            messages.error(request, resultado.get('message', 'Error al crear categoría'))
    
    return render(request, 'app/crear_categoria.html')

def crear_cliente(request):
    """Crear nuevo cliente"""
    if request.method == 'POST':
        datos = {
            'nit': request.POST['nit'],
            'nombre': request.POST['nombre'],
            'usuario': request.POST['usuario'],
            'clave': request.POST['clave'],
            'direccion': request.POST['direccion'],
            'correo_electronico': request.POST['correo_electronico']
        }
        resultado = BackendService.crear_cliente(datos)
        if resultado.get('success'):
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('consultar_datos')
        else:
            messages.error(request, resultado.get('message', 'Error al crear cliente'))
    
    return render(request, 'app/crear_cliente.html')

def cancelar_instancia(request):
    """Cancelar instancia de cliente"""
    if request.method == 'POST':
        nit_cliente = request.POST['nit_cliente']
        id_instancia = int(request.POST['id_instancia'])
        fecha_final = request.POST['fecha_final']
        
        resultado = BackendService.cancelar_instancia(nit_cliente, id_instancia, fecha_final)
        if resultado.get('success'):
            messages.success(request, 'Instancia cancelada exitosamente')
        else:
            messages.error(request, resultado.get('message', 'Error al cancelar instancia'))
    
    # Obtener clientes para el formulario
    clientes = BackendService.obtener_clientes()
    context = {
        'clientes': clientes.get('data', []) if clientes.get('success') else []
    }
    return render(request, 'app/cancelar_instancia.html', context)

# ==================== FACTURACIÓN ====================

def facturacion(request):
    """Proceso de facturación"""
    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        resultado = BackendService.generar_facturas(fecha_inicio, fecha_fin)
        
        if resultado.get('success'):
            facturas_generadas = len(resultado.get('data', []))
            messages.success(request, f'Se generaron {facturas_generadas} facturas exitosamente')
            return redirect('listar_facturas')
        else:
            messages.error(request, resultado.get('message', 'Error al generar facturas'))
    
    return render(request, 'app/facturacion.html')

def listar_facturas(request):
    """Listar todas las facturas"""
    facturas = BackendService.obtener_facturas()
    context = {
        'facturas': facturas.get('data', []) if facturas.get('success') else []
    }
    return render(request, 'app/listar_facturas.html', context)

# ==================== REPORTES PDF ====================

def reporte_factura_pdf(request, numero):
    """Generar PDF de detalle de factura"""
    from .pdf_generator import generar_pdf_factura
    
    facturas = BackendService.obtener_facturas()
    factura_data = None
    
    if facturas.get('success'):
        for factura in facturas.get('data', []):
            if factura.get('numero') == numero:
                factura_data = factura
                break
    
    if factura_data:
        pdf_buffer = generar_pdf_factura(factura_data)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="factura_{numero}.pdf"'
        return response
    else:
        messages.error(request, 'Factura no encontrada')
        return redirect('listar_facturas')

def reporte_analisis_ventas(request):
    """Análisis de ventas por categoría/recurso"""
    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        tipo_analisis = request.POST['tipo_analisis']
        
        if tipo_analisis == 'categorias':
            resultado = BackendService.analizar_ventas_categoria(fecha_inicio, fecha_fin)
        else:
            resultado = BackendService.analizar_ventas_recurso(fecha_inicio, fecha_fin)
        
        if resultado.get('success'):
            # Generar PDF
            from .pdf_generator import generar_pdf_analisis
            pdf_buffer = generar_pdf_analisis(
                resultado.get('data', []), 
                tipo_analisis, 
                fecha_inicio, 
                fecha_fin
            )
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            filename = f"analisis_{tipo_analisis}_{fecha_inicio}_a_{fecha_fin}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            messages.error(request, resultado.get('message', 'Error al generar análisis'))
    
    return render(request, 'app/reporte_analisis.html')

# ==================== AYUDA ====================

def informacion_estudiante(request):
    """Información del estudiante"""
    estudiante = {
        'nombre': 'Josue [Tu Nombre Completo]',
        'carnet': '202300814',
        'curso': 'IPC2 - Introducción a la Programación y Computación 2',
        'universidad': 'Universidad San Carlos de Guatemala',
        'facultad': 'Facultad de Ingeniería',
        'escuela': 'Escuela de Ciencias y Sistemas',
        'catedraticos': [
            'Inga. Claudia Liceth Rojas Morales',
            'Ing. Marlon Antonio Pérez Türk', 
            'Ing. José Manuel Ruiz Juárez',
            'Ing. Dennis Stanley Barrios González',
            'Ing. Edwin Estuardo Zapeta Gómez',
            'Ing. Fernando José Paz González'
        ],
        'tutores': [
            'Angely Naomi Marroquin Tapaz',
            'Diego Andrés Huite Alvarez',
            'Hesban Amilcar Argueta Aguilar', 
            'Pedro Luis Pu Tavico',
            'Angel Miguel García Urizar',
            'Luis Antonio Castillo Javier'
        ]
    }
    return render(request, 'app/informacion_estudiante.html', {'estudiante': estudiante})

def documentacion(request):
    """Documentación del programa"""
    return render(request, 'app/documentacion.html')

# ==================== VISTAS SIMPLES PARA PRUEBAS ====================

def vista_simple(request, template_name, page_title):
    """Vista genérica para templates simples"""
    return render(request, f'app/{template_name}', {'page_title': page_title})
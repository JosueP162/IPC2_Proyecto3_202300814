# [file name]: app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    
    # Enviar mensajes XML
    path('configuracion-xml/', views.configuracion_xml, name='configuracion_xml'),
    path('consumos-xml/', views.consumos_xml, name='consumos_xml'),
    
    # Operaciones del sistema
    path('inicializar-sistema/', views.inicializar_sistema, name='inicializar_sistema'),
    path('consultar-datos/', views.consultar_datos, name='consultar_datos'),
    
    # Creación de datos
    path('crear-recurso/', views.crear_recurso, name='crear_recurso'),
    path('crear-categoria/', views.crear_categoria, name='crear_categoria'),
    path('crear-cliente/', views.crear_cliente, name='crear_cliente'),
    path('cancelar-instancia/', views.cancelar_instancia, name='cancelar_instancia'),
    
    # Facturación
    path('facturacion/', views.facturacion, name='facturacion'),
    path('facturas/', views.listar_facturas, name='listar_facturas'),
    path('factura/<int:numero>/pdf/', views.reporte_factura_pdf, name='reporte_factura_pdf'),
    
    # Reportes PDF
    path('reporte-analisis/', views.reporte_analisis_ventas, name='reporte_analisis_ventas'),
    
    # Ayuda
    path('informacion-estudiante/', views.informacion_estudiante, name='informacion_estudiante'),
    path('documentacion/', views.documentacion, name='documentacion'),
]
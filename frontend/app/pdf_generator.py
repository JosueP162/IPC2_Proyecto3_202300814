# [file name]: app/pdf_generator.py
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

def generar_pdf_factura(factura_data):
    """Genera PDF con el detalle de una factura"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
    
    styles = getSampleStyleSheet()
    elements = []
    
    # Estilo para el título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Centrado
    )
    
    # Encabezado
    elements.append(Paragraph("TECNOLOGÍAS CHAPINAS, S.A.", title_style))
    elements.append(Paragraph("DETALLE DE FACTURA", styles['Heading2']))
    elements.append(Spacer(1, 20))
    
    # Información de la factura
    info_data = [
        ['Número de Factura:', str(factura_data.get('numero', ''))],
        ['NIT Cliente:', factura_data.get('nit_cliente', '')],
        ['Fecha:', factura_data.get('fecha', '')],
        ['Monto Total:', f"Q {factura_data.get('monto_total', 0):.2f}"]
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 30))
    
    # Detalles de la factura
    elements.append(Paragraph("DETALLE POR INSTANCIA", styles['Heading3']))
    elements.append(Spacer(1, 10))
    
    for detalle in factura_data.get('detalles', []):
        # Información de la instancia
        instancia_data = [
            ['Instancia:', detalle.get('nombre_instancia', '')],
            ['ID Instancia:', str(detalle.get('id_instancia', ''))],
            ['Horas Consumidas:', f"{detalle.get('horas_consumidas', 0):.2f}"],
            ['Costo Total:', f"Q {detalle.get('costo_total', 0):.2f}"]
        ]
        
        instancia_table = Table(instancia_data, colWidths=[1.5*inch, 3.5*inch])
        instancia_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
        ]))
        
        elements.append(instancia_table)
        elements.append(Spacer(1, 10))
        
        # Detalle de recursos por instancia
        recursos_data = [['Recurso', 'Cantidad', 'Horas', 'Costo']]
        for recurso in detalle.get('detalles_recursos', []):
            recursos_data.append([
                recurso.get('recurso', ''),
                str(recurso.get('cantidad', 0)),
                f"{recurso.get('horas', 0):.2f}",
                f"Q {recurso.get('costo', 0):.2f}"
            ])
        
        if len(recursos_data) > 1:
            recursos_table = Table(recursos_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch])
            recursos_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ]))
            elements.append(recursos_table)
        
        elements.append(Spacer(1, 20))
    
    # Pie de página
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Sistema de Facturación - Tecnologías Chapinas, S.A.", styles['Normal']))
    elements.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generar_pdf_analisis(datos_analisis, tipo_analisis, fecha_inicio, fecha_fin):
    """Genera PDF con análisis de ventas"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    styles = getSampleStyleSheet()
    elements = []
    
    # Título
    title = "ANÁLISIS DE VENTAS POR CATEGORÍA" if tipo_analisis == 'categorias' else "ANÁLISIS DE VENTAS POR RECURSO"
    elements.append(Paragraph(title, styles['Heading1']))
    elements.append(Paragraph(f"Período: {fecha_inicio} a {fecha_fin}", styles['Heading2']))
    elements.append(Spacer(1, 30))
    
    if not datos_analisis:
        elements.append(Paragraph("No hay datos para el período seleccionado.", styles['Normal']))
    else:
        # Preparar datos para la tabla
        if tipo_analisis == 'categorias':
            table_data = [['Categoría', 'Configuración', 'Ingresos (Q)', 'Instancias', 'Horas Totales']]
            for item in datos_analisis:
                table_data.append([
                    item.get('categoria_nombre', ''),
                    item.get('configuracion_nombre', ''),
                    f"{item.get('ingresos', 0):.2f}",
                    str(item.get('instancias_vendidas', 0)),
                    f"{item.get('horas_totales', 0):.2f}"
                ])
        else:
            table_data = [['Recurso', 'Ingresos (Q)', 'Horas Totales', 'Cantidad Total']]
            for item in datos_analisis:
                table_data.append([
                    item.get('recurso', ''),
                    f"{item.get('ingresos', 0):.2f}",
                    f"{item.get('horas_totales', 0):.2f}",
                    f"{item.get('cantidad_total_usada', 0):.2f}"
                ])
        
        # Crear tabla
        table = Table(table_data, colWidths=[2*inch, 2*inch, 1.5*inch, 1*inch, 1.5*inch] if tipo_analisis == 'categorias' else [3*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        
        elements.append(table)
    
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Reporte generado automáticamente - Tecnologías Chapinas, S.A.", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
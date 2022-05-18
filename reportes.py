from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os
from arrow import utcnow


class ReciboFactura:
    """Objeto para crear un recibo asociado a una factura"""

    def __init__(self):
        """Inicializa el titulo de la factura"""
        self.titulo = 'Factura.pdf'
        self.factura = canvas.Canvas(self.titulo, pagesize=A4)

    def crear_esqueleto(self):
        _, h = A4
        self.factura
        fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
        fechaReporte = fecha.replace("-", "de")
        self.factura.setFont("Times-Roman", 10)
        self.factura.drawString(90, h - 105, str(fechaReporte))
        self.factura.drawString(385, h - 105, str(fechaReporte))

        # ORIGINAL
        self.factura.setFont("Times-Roman", 12)
        self.factura.drawString(90, h - 20, 'BAR RESTAURANT')
        self.factura.setFont("Times-Roman", 11)
        self.factura.drawString(105, h - 30, '"La Paila Brava"')
        self.factura.setFont("Times-Roman", 12)
        self.factura.drawString(100, h - 45, 'TICKET No.')
        self.factura.line(x1=20, x2=270, y1=h - 50, y2=h - 50)
        self.factura.setFont("Times-Roman", 10)
        self.factura.drawString(20, h - 60, 'NOMBRE        :')
        self.factura.drawString(20, h - 75, 'No. CÉDULA  :')
        self.factura.drawString(20, h - 90, 'DIRECCIÓN   :')
        self.factura.drawString(20, h - 105, 'F. EMISIÓN    :')
        self.factura.line(x1=20, x2=270, y1=h - 110, y2=h - 110)
        self.factura.drawString(90, h - 125, "DETALLE DEL TICKET")

        # CLIENTE
        self.factura.setFont("Times-Roman", 12)
        self.factura.drawString(385, h - 20, 'BAR RESTAURANT')
        self.factura.setFont("Times-Roman", 11)
        self.factura.drawString(400, h - 30, '"La Paila Brava"')
        self.factura.setFont("Times-Roman", 12)
        self.factura.drawString(395, h - 45, 'TICKET No.')
        self.factura.line(x1=315, x2=565, y1=h - 50, y2=h - 50)
        self.factura.setFont("Times-Roman", 10)
        self.factura.drawString(315, h - 60, 'NOMBRE        :')
        self.factura.drawString(315, h - 75, 'No. CÉDULA  :')
        self.factura.drawString(315, h - 90, 'DIRECCIÓN   :')
        self.factura.drawString(315, h - 105, 'F. EMISIÓN    :')
        self.factura.line(x1=315, x2=565, y1=h - 110, y2=h - 110)
        self.factura.drawString(385, h - 125, "DETALLE DEL TICKET")

    def dibujar_tabla(self, lista_productos):
        _, h = A4
        centinela = 0
        data = [['Prod.', 'Cant.', 'P.V.P', 'Subt.'],
                ]
        for productos in lista_productos:
            lista = []
            lista.append(str(productos.nombre))
            lista.append(str(productos.cantidad))
            lista.append(str(productos.precio_venta))
            lista.append(str(productos.sub_total))
            data.append(lista)
            centinela = centinela + 20

        table = Table(data, colWidths=[150, 30, 40, 30], )
        table.setStyle(TableStyle(
            [
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ])
        )

        punto_separacion = h - 150 - centinela
        table.wrapOn(self.factura, 100, 100)
        table.drawOn(self.factura, x=20, y=h - 145 - centinela)
        table.drawOn(self.factura, x=315, y=h - 145 - centinela)

        self.factura.setFont("Times-Roman", 11)
        self.factura.drawString(195, punto_separacion - 10, 'TOTAL $: ')
        self.factura.drawString(200, punto_separacion - 22, ' PAGO $: ')
        self.factura.drawString(189, punto_separacion - 34, 'CAMBIO $: ')

        self.factura.setFont("Times-Roman", 11)
        self.factura.drawString(490, punto_separacion - 10, 'TOTAL $: ')
        self.factura.drawString(495, punto_separacion - 22, ' PAGO $: ')
        self.factura.drawString(484, punto_separacion - 34, 'CAMBIO $: ')

        return punto_separacion

    def detalles_factura(self, object):
        obj_factura = object
        punto = self.dibujar_tabla(obj_factura.lista_productos)
        self.crear_esqueleto()
        self.llenar_factura(obj_factura, punto)

    def llenar_factura(self, object, punto):
        w, h = A4
        self.factura.setFont("Times-Roman", 12)
        self.factura.drawString(190, h - 45, str(object.id_factura))
        self.factura.setFont("Times-Roman", 10)
        self.factura.drawString(90, h - 60, str(object.nom_ape_cl))
        self.factura.drawString(90, h - 75, str(object.id_cliente))
        self.factura.drawString(90, h - 90, str(object.dir_cl))
        self.factura.setFont("Times-Roman", 10)
        self.factura.drawString(245, punto - 10, str(object.total))
        self.factura.drawString(245, punto - 22, str(object.pago))
        self.factura.drawString(245, punto - 34, str(object.cambio))

        self.factura.setFont("Times-Roman", 12)
        self.factura.drawString(485, h - 45, str(object.id_factura))
        self.factura.setFont("Times-Roman", 10)
        self.factura.drawString(385, h - 60, str(object.nom_ape_cl))
        self.factura.drawString(385, h - 75, str(object.id_cliente))
        self.factura.drawString(385, h - 90, str(object.dir_cl))
        self.factura.setFont("Times-Roman", 10)
        self.factura.drawString(545, punto - 10, str(object.total))
        self.factura.drawString(545, punto - 22, str(object.pago))
        self.factura.drawString(545, punto - 34, str(object.cambio))

    def save(self):
        self.factura.showPage()
        self.factura.save()
        os.system(self.titulo)

    def __del__(self):
        pass

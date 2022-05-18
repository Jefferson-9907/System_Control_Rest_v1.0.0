from tkinter import messagebox

from funciones_auxiliares import conexion_consulta
from reportes import ReciboFactura


class Producto:

    def __init__(self, *args, **kwargs):

        self.id = None
        self.nombre = None
        self.precio_compra = None
        self.precio_venta = None
        self.stock = None
        self.estado = None

    def seleccionar(self):
        consulta = 'SELECT * FROM INV_PRODUCTO WHERE id=?'
        parametros = [self.id]
        return conexion_consulta(consulta, parametros)

    def guardar(self):
        consulta = 'INSERT INTO INV_PRODUCTO VALUES(?, ?, ?, ?, ?, ?)'
        parametros = [(parametro[1]) for parametro in self.__dict__.items()]

        return conexion_consulta(consulta, parametros)

    def actualizar(self):
        consulta = '''UPDATE INV_PRODUCTO set id=?, nombre=?, precio_compra=?,
                    precio_venta=?, inventario=?, estado=? WHERE id=?
                    '''
        parametros = [(parametro[1]) for parametro in self.__dict__.items()]
        parametros.append(self.id)
        print(parametros)

        return conexion_consulta(consulta, parametros)

    def eliminar(self):
        ask = messagebox.askyesno("SYST_CONTROL(REST®)-->(CONFIRMACIÓN ELIMINAR)",
                                  f"DESEA ELIMINAR PRODUCTO: {self.nombre}")
        if ask is True:
            consulta = 'DELETE FROM INV_PRODUCTO WHERE id=?'
            parametros = [self.id]
            conexion_consulta(consulta, parametros)
            messagebox.showinfo("SYST_CONTROL(REST®)-->(ELIMINACIÓN)",
                                f"DATOS DEL PRODUCTO: {self.nombre}\n"
                                f"ELIMINADOS DEL REGISTRO CORRECTAMENTE!!!")

        else:
            pass

    def inactivar(self):
        consulta = 'UPDATE INV_PRODUCTO set estado=? WHERE id=?'
        parametros = [self.estado, self.id]
        return conexion_consulta(consulta, parametros)

    def validar(self):  # Metodo que valida que los inputs no ingrese valores nulos
        atributos = self.__dict__.items()
        centinela = True

        for datos in atributos:
            if datos[1] == '':
                centinela = False
                break
            elif datos[1] is not None:
                centinela = True

        return centinela


class ProductoFacturar(Producto):

    def __init__(self, *args, **kwargs):
        super(Producto, self).__init__(*args, **kwargs)
        self.id_factura = ''
        self.cantidad = 0
        self.sub_total = 0

    def calcular_subtotal(self):
        return self.precio_venta * self.cantidad

    def convertir_dic(self):
        return {'codigo': self.id,
                'nombre': self.nombre,
                'precio_venta': self.precio_venta,
                'cantidad': self.cantidad,
                'sub-total': self.sub_total
                }

    def guardar(self):
        consulta = 'INSERT INTO FCT_DETALLE_FACT VALUES(?, ?, ?, ?, ?)'
        parametros = [self.id_factura, self.id, self.precio_venta, self.cantidad, self.sub_total]
        conexion_consulta(consulta, parametros)
        self.reducir_existencia()

    def reducir_existencia(self):
        producto_reducir = self.seleccionar()
        for producto_reducido in producto_reducir:
            stock = int(producto_reducido[4])

        nuevo_stock = stock - self.cantidad

        consulta = 'UPDATE INV_PRODUCTO set inventario=? WHERE id=?'
        parametros = [nuevo_stock, self.id]
        conexion_consulta(consulta, parametros)


class Factura(ReciboFactura):

    def __init__(self, *args, **kwargs):
        super(Factura, self).__init__(*args, **kwargs)

        self.id_factura = ''
        self.id_cliente = ''
        self.fecha_creacion = ''
        self.hora_creacion = ''
        self.lista_productos = []
        self.total = 0
        self.pago = 0
        self.cambio = 0

    def guardar(self):
        consulta = 'INSERT INTO FCT_FACTURA VALUES(?, ?, ?, ?, ?, ?, ?)'
        parametros = [
            self.id_factura, self.id_cliente, self.fecha_creacion,
            self.hora_creacion, self.total, self.pago, self.cambio
        ]
        conexion_consulta(consulta, parametros)

    def remover_producto(self, nombre):
        for lista_productos in self.lista_productos:
            if nombre == lista_productos.nombre:
                self.lista_productos.remove(lista_productos)
        return True

    def calcular_total(self):
        total = 0
        for sub_total in self.lista_productos:
            total = float(sub_total.calcular_subtotal()) + total
        self.total = total
        return total


class Cliente:

    def __init__(self, *args, **kwargs):
        self.id = ''
        self.nombre = ''
        self.n_celular = ''
        self.direccion = ''

    def guardar(self):
        consulta = 'INSERT INTO INV_CLIENTE VALUES (?, ?, ?, ?)'
        parametros = [self.id, self.nombre, self.n_celular, self.direccion]
        conexion_consulta(consulta, parametros)


class Apertura:
    def __init__(self, *args, **kwargs):
        self.id = ''
        self.cantidad = ''
        self.fecha_creacion = ''

    def g_apertura(self):
        consulta = 'INSERT INTO INV_APERTURA_CAJA VALUES (?, ?, ?)'
        parametros = [self.id, self.cantidad, self.fecha_creacion]
        conexion_consulta(consulta, parametros)


class Ingresos:
    def __init__(self, *args, **kwargs):
        self.cantidad = ''
        self.fecha = ''

    def g_ingresos(self):
        consulta = 'INSERT INTO INV_INGRESOS VALUES (?, ?)'
        parametros = [self.cantidad, self.fecha]
        conexion_consulta(consulta, parametros)


class Egresos:
    def __init__(self, *args, **kwargs):
        self.cantidad = ''
        self.fecha = ''

    def g_egresos(self):
        consulta = 'INSERT INTO INV_EGRESOS VALUES (?, ?)'
        parametros = [self.cantidad, self.fecha]
        conexion_consulta(consulta, parametros)


class Cierre_caja:
    def __init__(self, *args, **kwargs):
        self.apertura = ''
        self.ingresos = ''
        self.egresos = ''
        self.total_caja = ''
        self.fecha = ''

    def g_cierre_caja(self):
        consulta = 'INSERT INTO INV_CIERRE_CAJA VALUES (?, ?, ?, ?, ?)'
        parametros = [self.apertura, self.ingresos, self.egresos, self.total_caja, self.fecha]
        conexion_consulta(consulta, parametros)


class Proveedor:

    def __init__(self, *args, **kwargs):
        self.id = ''
        self.nombres = ''
        self.n_celular = ''
        self.direccion = ''

    def guardar(self):
        consulta = 'INSERT INTO INV_PROVEEDOR VALUES (?, ?, ?, ?)'
        parametros = [self.id, self.nombres, self.n_celular, self.direccion]
        conexion_consulta(consulta, parametros)
        messagebox.showinfo("SYST_CONTROL(REST®)-->(ÉXITO)",
                            f"PROVEEDOR: {self.nombres}\nREGISTRADO CORRECTAMENTE")

    def actualizar(self):
        consulta = 'UPDATE INV_PROVEEDOR SET nombres=?, n_celular=?, direccion=? WHERE id_proveedor=?'
        parametros = [self.nombres, self.n_celular, self.direccion, self.id]
        conexion_consulta(consulta, parametros)
        messagebox.showinfo("SYST_CONTROL(REST®)-->(ÉXITO)",
                            f"DATOS DEL PROVEEDOR: {self.nombres}\nACTUALIZADOS REGISTRO CORRECTAMENTE")

    def eliminar(self):
        ask = messagebox.askyesno("SYST_CONTROL(REST®)-->(CONFIRMACIÓN ELIMINAR)",
                                  f"DESEA ELIMINAR PROVEEDOR: {self.nombres}")
        if ask is True:
            consulta = 'DELETE FROM INV_PROVEEDOR WHERE id_proveedor=?'
            parametros = [self.id]
            conexion_consulta(consulta, parametros)
            messagebox.showinfo("SYST_CONTROL(REST®)-->(ELIMINACIÓN)",
                                f"DATOS DEL PROVEEDOR: {self.nombres}\n"
                                f"ELIMINADOS DEL REGISTRO CORRECTAMENTE!!!")

        else:
            pass


class Materia_prima:

    def __init__(self, *args, **kwargs):
        self.id = None
        self.descripcion = None
        self.cantidad = None
        self.observacion = None

    def guardar(self):
        consulta = 'INSERT INTO INV_MATERIA_P VALUES (?, ?, ?, ?)'
        parametros = [self.id, self.descripcion, self.cantidad, self.observacion]
        conexion_consulta(consulta, parametros)
        messagebox.showinfo("SYST_CONTROL(REST®)-->(ÉXITO)",
                            f"DATOS DE MATERIA PRIMA: {self.descripcion}\nREGISTRADOS CORRECTAMENTE")

    def actualizar(self):
        consulta = 'UPDATE INV_MATERIA_P SET descripcion=?, stock=?, observacion=? WHERE id_materia_prima=?'
        parametros = [self.descripcion, self.cantidad, self.observacion, self.id]
        conexion_consulta(consulta, parametros)
        messagebox.showinfo("SYST_CONTROL(REST®)-->(ÉXITO)",
                            f"DATOS DE MATERIA PRIMA: {self.descripcion}\nACTUALIZADOS REGISTRO CORRECTAMENTE")

    def eliminar(self):
        ask = messagebox.askyesno("SYST_CONTROL(REST®)-->(CONFIRMACIÓN ELIMINAR)",
                                  f"DESEA ELIMINAR MATERIA PRIMA: {self.descripcion}")
        if ask is True:
            consulta = 'DELETE FROM INV_MATERIA_P WHERE descripcion=?'
            parametros = [self.descripcion]
            conexion_consulta(consulta, parametros)
            messagebox.showinfo("SYST_CONTROL(REST®)-->(ELIMINACIÓN)",
                                f"DATOS DE MATERIA PRIMA: {self.descripcion}\n"
                                f"ELIMINADOS DEL REGISTRO CORRECTAMENTE!!!")

        else:
            pass

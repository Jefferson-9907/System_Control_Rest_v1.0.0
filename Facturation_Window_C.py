from tkinter import *
from tkinter.ttk import Treeview, Combobox
from ttkthemes import themed_tk as tk
from tkinter import messagebox
import random
from datetime import datetime
from time import strftime

import Password_Window_C
import Principal_Window_C

"""import Re_Facturation"""
import Re_Facturation_F
import login_form
from modelos import Producto, ProductoFacturar, Factura, Cliente
from funciones_auxiliares import solo_numero, conexion_consulta
from reportes import ReciboFactura


class Facturation:
    """
        Contiene todos los widgets necesario para la facturacion
    """

    def __init__(self, root):

        self.root = root
        self.root.title("SYST_CONTROL(REST®)--›(Venta)")
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.iconbitmap('recursos\\icon_rest.ico')
        self.root.configure(bg='#a27114')

        self.imagenes = {
            'nuevo': PhotoImage(file='recursos\\icon_add.png'),
            'editar': PhotoImage(file='recursos\\icon_update.png'),
            'eliminar': PhotoImage(file='recursos\\icon_delete.png'),
            'inactivar': PhotoImage(file='recursos\\icon_warr.png'),
            'reportes': PhotoImage(file='recursos\\icon_up.png'),
            'new': PhotoImage(file='recursos\\icon_new_ind.png'),
            'buscar': PhotoImage(file='recursos\\icon_buscar.png'),
            'todo': PhotoImage(file='recursos\\icon_ver_todo.png'),
            'facturar': PhotoImage(file='recursos\\icon_aceptar.png'),
            'actualizar': PhotoImage(file='recursos\\icon_upd.png'),
            'print': PhotoImage(file='recursos\\icon_fact.png')

        }

        # =============================================================
        # BANNER PANTALLA FACTURACIÓN
        # =============================================================

        self.txt = "SYSTEM CONTROL REST® (TÍCKET)"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("Cooper Black", 35), bg="#000000",
                             fg='black', bd=5, relief=FLAT)
        self.heading.place(x=0, y=0, width=1367)

        self.slider()
        self.heading_color()

        # =============================================================
        # CREACIÓN DE LA BARRA DE MENÚ
        # =============================================================
        self.menubarra = Menu(self.root)

        # =============================================================
        # CREACIÓN DEL MENÚ ALUMNO
        # =============================================================
        self.menubarra.add_cascade(label='RESTAURANT')
        self.root.config(menu=self.menubarra)
        self.menus = Menu(self.root)
        self.Column1 = Menu(self.menus, tearoff=0)

        # =============================================================
        # AÑADIENDO OPCIONES AL MENÚ PRINCIPAL
        # =============================================================
        self.menus.add_cascade(label='INICIO', menu=self.Column1)
        self.Column1.add_command(label='Menú Inicio', command=self.principal_btn)
        self.Column2 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ FACTURACIÓN
        # =============================================================
        self.menus.add_cascade(label='VENTA', menu=self.Column2)
        self.Column2.add_command(label='Tícket')
        self.Column2.add_command(label='Verificar Tícket', command=self.ver_fct_btn)
        self.Column3 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ AYUDA
        # =============================================================
        self.menus.add_cascade(label='USUARIOS', menu=self.Column3)
        self.Column3.add_command(label='Cambiar Usuario', command=self.logout)
        self.Column3.add_command(label='Cambiar Contraseña', command=self.pass_btn)
        self.Column3.add_separator()
        self.Column3.add_command(label='Cerrar Sesión', command=self.salir_principal)
        self.Column3.add_separator()
        self.Column4 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ INFO
        # =============================================================
        self.menus.add_cascade(label='INFO', menu=self.Column4)
        self.Column4.add_command(label='Sobre SIST_CONTROL (REST®)', command=self.caja_info_sist)
        self.Column4.add_separator()
        self.root.config(menu=self.menus)

        self.footer_4 = Label(self.root, text='J.C.F DESING® | Derechos Reservados 2022', width=195, bg='black',
                              fg='white')
        self.footer_4.place(x=0, y=725)

        data = datetime.now()
        fomato_f = " %A %d/%B/%Y"

        self.footer = Label(self.root, text='  FECHA Y HORA: ', font=("Cooper Black", 9), bg='black',
                            fg='white')
        self.footer.place(x=930, y=725)
        self.footer_1 = Label(self.root, text=str(data.strftime(fomato_f)), font=("Lucida Console", 10), bg='black',
                              fg='white')
        self.footer_1.place(x=1040, y=727)

        self.clock = Label(self.root)
        self.clock['text'] = '00:00:00'
        self.clock['font'] = 'Tahoma 9 bold'
        self.clock['bg'] = 'black'
        self.clock['fg'] = 'white'
        self.clock.place(x=1275, y=725)
        self.tic()
        self.tac()

        self.widget_menu()  # Invoca los metodos para
        self.widget_buscar()  # crear los widget de cada
        self.ventana_productos()  # Seccion Productos
        self.listar_productos()
        self.factura = Factura()

        self.validatecommand = self.root.register(solo_numero)
        self.validate_subtotal = self.root.register(self.mostrar_sub_total)
        self.nueva_factura()

    def tic(self):
        self.clock["text"] = strftime("%H:%M:%S %p")

    def tac(self):
        self.tic()
        self.clock.after(1000, self.tac)

    def slider(self):
        """creates slides for heading by taking the text,
        and that text are called after every 100 ms"""
        if self.count >= len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)

        else:
            self.text = self.text + self.txt[self.count]
            self.heading.config(text=self.text)
        self.count += 1

        self.heading.after(100, self.slider)

    def heading_color(self):
        """
        configures heading label
        :return: every 50 ms returned new random color.

        """
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(50, self.heading_color)

    def widget_menu(self):
        """
         Botones asociados en la barra superior acerca del estado
         de los productos
        """

        self.label_producto = LabelFrame(self.root, text='Opciones del inventario', bg='#a27114', width=520, height=90)
        self.label_producto.place(x=15, y=80)

        self.Btnproducto = Button(self.label_producto, image=self.imagenes['nuevo'], text='Nuevo', bg='#a27114',
                                  command=self.widgets_producto, compound=TOP)
        self.Btnproducto.image = self.imagenes['nuevo']
        self.Btnproducto.place(x=5, y=5)

        self.Btneditar = Button(self.label_producto, image=self.imagenes['editar'],
                                command=self.widget_buscar_producto, text='Editar', bg='#a27114', compound=TOP)
        self.Btneditar.image = self.imagenes['editar']
        self.Btneditar.place(x=74, y=5)

        self.Btninactivar = Button(self.label_producto, image=self.imagenes['eliminar'],
                                   command=self.inactivar_producto, text='Inactivar', bg='#a27114', compound=TOP)
        self.Btninactivar.image = self.imagenes['eliminar']
        self.Btninactivar.place(x=139, y=5)

        self.BtnReportes = Button(self.label_producto, image=self.imagenes['reportes'],
                                  command=self.listar_productos, text='Refrescar', bg='#a27114', compound=TOP)
        self.BtnReportes.image = self.imagenes['reportes']
        self.BtnReportes.place(x=223, y=5)

        fecha = datetime.now()
        fecha_conv = '{} - {} - {}'.format(fecha.day, fecha.month, fecha.year)

        self.lb_fecha = Label(self.label_producto, text='FECHA :')
        self.lb_fecha.place(x=640, y=5)

        self.lb_fecha_actual = Label(self.label_producto, text=fecha_conv)
        self.lb_fecha_actual.place(x=700, y=5)

    def widget_buscar(self):
        """
            Widgets asociados a la busqueda de un producto
        """
        self.labelframe_buscador = LabelFrame(self.root, text="Buscar", bg='#a27114', width=520, height=60)
        self.labelframe_buscador.place(x=15, y=175)
        self.l_Buscar = Label(self.labelframe_buscador, text="BUSCAR :", bg='#a27114', fg="White",
                              font=("Copperplate Gothic Bold", 10, "bold"))
        self.l_Buscar.place(x=5, y=2)
        self.busc = StringVar()
        self.txtBuscar = Entry(self.labelframe_buscador, textvariable=self.busc, width=35)
        self.txtBuscar.place(x=90, y=5)
        self.txtBuscar.bind('<Return>', self.buscar_productos)

        self.btnBuscar = Button(self.labelframe_buscador, image=self.imagenes['buscar'], text='BUSCAR', width=80,
                                command=lambda: self.buscar_productos(1), compound="right")
        self.btnBuscar.image = self.imagenes['buscar']
        self.btnBuscar.place(x=320, y=0)

        self.Btnview = Button(self.labelframe_buscador, image=self.imagenes['todo'], command=self.listar_productos,
                              text='Ver Todo', compound="right")
        self.Btnview.image = self.imagenes['todo']
        self.Btnview.place(x=425, y=0)

    def buscar_productos(self, event):
        """
            Funcion asociada a widget buscar para la busqueda de un
            producto
        """
        varia = str(self.txtBuscar.get())
        consulta = "SELECT * FROM producto WHERE nombre LIKE '%' || ? ||'%'"
        parametros = [varia]

        producto_qs = conexion_consulta(consulta, parametros)

        if producto_qs:
            p = producto_qs
            self.llenar_registros(p)

    def ventana_productos(self):
        """
         Widget que muestra los productos en general
         o ya filtrado en una busqueda
        """
        self.labelproductos = LabelFrame(self.root, width=520, height=450, text='Productos', bg='#a27114')
        self.labelproductos.place(x=15, y=240)
        self.listdetalle = Treeview(self.labelproductos, columns=('#0', '#1', '#2'), height=19)

        self.listdetalle.column('#0', width=75)
        self.listdetalle.column('#1', width=320)
        self.listdetalle.column('#2', width=50)
        self.listdetalle.column('#3', width=50)

        self.listdetalle.heading('#0', text='Cod.')
        self.listdetalle.heading('#1', text='Producto_w')
        self.listdetalle.heading('#2', text='Precio')
        self.listdetalle.heading('#3', text='Stock')

        self.listdetalle.place(x=10, y=10)

    def widget_buscar_producto(self):
        """
         Ventana hija para buscar un producto
         y actualizarlo
        """
        self.VtBuscar = Toplevel()
        self.VtBuscar.geometry('300x55')
        self.VtBuscar.title("SYST_CONTROL(REST®)--›(Editar u Eliminar)")
        self.VtBuscar.grab_set()
        self.VtBuscar.transient(master=self.root)

        # Manage Frame
        self.Manage_Frame_b = Frame(self.VtBuscar, relief=RIDGE, bd=4, bg='#a27114')
        self.Manage_Frame_b.place(x=0, y=0, width=300, height=55)

        # Widgets para añadir un producto
        self.lbCodigoED = Label(self.Manage_Frame_b, text='COD:', font=("Copperplate Gothic Bold", 10, "bold"),
                                bg='#a27114', fg="White")
        self.lbCodigoED.place(x=5, y=10)
        self.txtCodigoED = Entry(self.VtBuscar, width=20)
        self.txtCodigoED.place(x=60, y=15)

        # Botones
        self.btnED = Button(self.Manage_Frame_b, image=self.imagenes['buscar'], text='BUSCAR', width=80,
                            command=self.actualizar_producto, compound="right")
        self.btnED.image = self.imagenes['buscar']
        self.btnED.place(x=190, y=5)

    def widgets_producto(self):
        """
         Ventana hija asociada al boton nuevo que funciona para
         agregar o modifcar un producto
        """
        self.nuevo_producto = Toplevel()
        self.nuevo_producto.title("SYST_CONTROL(REST®)--›(Nuevo producto)")
        self.nuevo_producto.geometry('415x280')
        self.nuevo_producto.configure(bg='#a27114')
        self.nuevo_producto.iconbitmap('recursos\\icon_rest.ico')
        self.nuevo_producto.transient(master=self.root)
        self.nuevo_producto.grab_set()

        # Manage Frame
        self.Manage_Frame = LabelFrame(self.nuevo_producto, width=385, height=250, bg='#a27114')
        self.Manage_Frame.place(x=15, y=15)

        # Widgets para añadir un producto
        self.lbCodigo = Label(self.Manage_Frame, text='COD:', font=("Copperplate Gothic Bold", 10, "bold"),
                              bg='#808080')
        self.lbCodigo.place(x=87, y=20)
        self.txtCodigo = Entry(self.Manage_Frame, width=10)
        self.txtCodigo.place(x=140, y=20)

        self.lbNombre = Label(self.Manage_Frame, text='DESCRIPCIÓN:', font=("Copperplate Gothic Bold", 10, "bold"),
                              bg='#808080')
        self.lbNombre.place(x=8, y=50)
        self.txtNombre = Entry(self.Manage_Frame, width=35)
        self.txtNombre.place(x=140, y=50)

        self.lbPrecio_compra = Label(self.Manage_Frame, text='P. COMPRA $:',
                                     font=("Copperplate Gothic Bold", 10, "bold"), bg='#808080')
        self.lbPrecio_compra.place(x=15, y=80)
        self.txtPrecio_compra = Entry(self.nuevo_producto, width=10, validate='key',
                                      validatecommand=(self.validatecommand, "%S"))
        self.txtPrecio_compra.place(x=157, y=97)

        self.lbPrecio_venta = Label(self.Manage_Frame, text='P.V.P. $:', font=("Copperplate Gothic Bold", 10, "bold"),
                                    bg='#808080')
        self.lbPrecio_venta.place(x=60, y=110)
        self.txtPrecio_venta = Entry(self.nuevo_producto, width=10, validate='key',
                                     validatecommand=(self.validatecommand, "%S"))
        self.txtPrecio_venta.place(x=157, y=127)

        self.lbStock = Label(self.Manage_Frame, text='STOCK:', font=("Copperplate Gothic Bold", 10, "bold"),
                             bg='#808080')
        self.lbStock.place(x=65, y=140)
        self.txtStock = Entry(self.nuevo_producto, width=10, validate='key',
                              validatecommand=(self.validatecommand, "%S"))
        self.txtStock.place(x=157, y=157)

        self.estado = Label(self.Manage_Frame, text='ESTADO :', font=("Copperplate Gothic Bold", 10, "bold"),
                            bg='#808080')
        self.estado.place(x=50, y=170)
        self.valor = BooleanVar()
        self.txtEstado = Checkbutton(self.nuevo_producto, variable=self.valor, onvalue=True, offvalue=False,
                                     bg='#a27114')
        self.txtEstado.place(x=156, y=187)

        # Botones
        self.BtnGuardar = Button(self.nuevo_producto, image=self.imagenes['nuevo'], text='GUARDAR', width=80,
                                 command=lambda: self.crear_o_editar_producto(1), compound="right")
        self.BtnGuardar.image = self.imagenes['nuevo']
        self.BtnGuardar.place(x=150, y=215)

    def widget_facturacion(self):
        """
         Ventana que asocia todos los controles e informacion
         acerca de la facturacion de un producto, no disponible cuando
         inicia, para acceder a ella presionar el boton nueva venta
        """
        self.label_facturacion = LabelFrame(self.root, width=800, height=605, bg='#a27114')
        self.label_facturacion.place(x=550, y=85)

        self.lb_cod_factura = Label(self.label_facturacion, text='No. TICKET:')
        self.lb_cod_factura.place(x=420, y=10)

        self.codigo_factura = IntVar()
        try:
            consulta = 'SELECT (id_factura+1) FROM FCT_FACTURA ORDER BY id_factura DESC LIMIT 1'
            codigo = conexion_consulta(consulta, parametros=())
            for values in codigo:
                data_list_id = values[0]
                self.codigo_factura.set(data_list_id)

        except BaseException as msg:
            print(msg)
        self.txt_cod_factura = Entry(self.label_facturacion, state='readonly', textvariable=self.codigo_factura,
                                     fg='Red', width=14, font=('Copperplate Gothic Bold', 14), relief=RIDGE)
        self.txt_cod_factura.place(x=580, y=10)

        self.label_facturacion_1 = LabelFrame(self.root, text='Datos para ticket', width=760, height=100,
                                              bg='#a27114')
        self.label_facturacion_1.place(x=570, y=130)

        self.search_field = StringVar()
        self.l_ced_al = Label(self.label_facturacion_1, text='No. CÉDULA', font=('Copperplate Gothic Bold', 10),
                              bg='#808080')
        self.l_ced_al.place(x=10, y=10)
        self.cliente = Entry(self.label_facturacion_1, textvariable=self.search_field, width=19)
        self.cliente.focus()
        self.cliente.place(x=110, y=10)

        self.btnBuscar = Button(self.label_facturacion_1, image=self.imagenes['buscar'], text='BUSCAR', width=80,
                                command=self.obtener_clientes, compound=RIGHT)
        self.btnBuscar.image = self.imagenes['buscar']
        self.btnBuscar.place(x=245, y=5)

        self.btn_add_clte = Button(self.label_facturacion_1, image=self.imagenes['nuevo'], text='AGREGAR', width=80,
                                   command=self.widget_cliente, compound=RIGHT)
        self.btn_add_clte.image = self.imagenes['nuevo']
        self.btn_add_clte.place(x=350, y=5)

        self.l_name = Label(self.label_facturacion_1, text='NOMBRES', font=('Copperplate Gothic Bold', 10), width=10,
                            bg='#808080')
        self.l_name.place(x=10, y=40)
        self.nombres_al = StringVar()
        self.name_e = Entry(self.label_facturacion_1, width=45, textvariable=self.nombres_al, state='readonly')
        self.nombres_al.set("Consumidor Final")
        self.name_e.place(x=110, y=40)

        self.lb_direccion = Label(self.label_facturacion_1, text='DIRECCIÓN', font=('Copperplate Gothic Bold', 10),
                                  bg='#808080', width=10)
        self.lb_direccion.place(x=390, y=40)
        self.direcccion_al = StringVar()
        self.dir_e_al = Entry(self.label_facturacion_1, width=40, textvariable=self.direcccion_al, state='readonly')
        self.direcccion_al.set("")
        self.dir_e_al.place(x=490, y=40)

        self.lb_detalle = Label(self.label_facturacion, text='-------DETALLE TICKET-------', bg='#a27114', fg="White",
                                font=("Copperplate Gothic Bold", 16, "bold"))
        self.lb_detalle.place(x=245, y=160)

        self.detalle_factura = Treeview(self.label_facturacion, columns=('#0', '#1', '#2',), height=10)
        self.detalle_factura.place(x=20, y=200)
        self.detalle_factura.column('#0', width=500)
        self.detalle_factura.column('#1', width=75)
        self.detalle_factura.column('#2', width=75)
        self.detalle_factura.column('#3', width=75)

        self.detalle_factura.heading('#0', text='Producto_w')
        self.detalle_factura.heading('#1', text='Cant.')
        self.detalle_factura.heading('#2', text='Precio')
        self.detalle_factura.heading('#3', text='Subtotal')

        self.detalle_factura.bind('<Double-1>', self.eliminar_item)  # Evento que permite eliminar
        # elemento del detalle de factura

        self.total = DoubleVar()
        self.lb_total = Label(self.label_facturacion, text='TOTAL    $', font=("Copperplate Gothic Bold", 11, "bold"),
                              bg='#a27114', fg="White")
        self.lb_total.place(x=610, y=475)
        self.tx_total = Entry(self.label_facturacion, state='readonly', textvariable=self.total, width=10)
        self.tx_total.place(x=711, y=475)

        self.lb_pago = Label(self.label_facturacion, text='PAGO      $', font=("Copperplate Gothic Bold", 11, "bold"),
                             bg='#a27114', fg="White")
        self.lb_pago.place(x=610, y=505)
        self.pago_f = DoubleVar()
        self.txt_pago = Entry(self.label_facturacion, validate='key', validatecommand=(self.validatecommand, "%S"),
                              textvariable=self.pago_f, width=10)
        self.txt_pago.place(x=711, y=505)

        self.cambio = StringVar()
        self.lb_cambio = Label(self.label_facturacion, text='CAMBIO $', font=("Copperplate Gothic Bold", 11, "bold"),
                               bg='#a27114', fg="White")
        self.lb_cambio.place(x=610, y=535)
        self.tx_cambio = Entry(self.label_facturacion, state='readonly', textvariable=self.cambio, width=10)
        self.tx_cambio.place(x=711, y=535)
        self.txt_pago.bind('<Return>', self.calcular_cambio)

        self.lb_moneda = Label(self.label_facturacion, text='Moneda', font=("Copperplate Gothic Bold", 11, "bold"),
                               bg='#a27114', fg="White")
        self.lb_moneda.place(x=400, y=475)
        self.tipo_moneda = Combobox(self.label_facturacion, values=['$-USD'], width=10)
        self.tipo_moneda.place(x=490, y=475)

        self.BtnFacturar = Button(self.label_facturacion, image=self.imagenes['print'], text='GUARDAR', width=80,
                                  command=self.guardar_factura, compound=TOP)
        self.BtnFacturar.image = self.imagenes['print']
        self.BtnFacturar.place(x=490, y=505)

    def eliminar_item(self):
        self.detalle_factura.delete(self.codigo.get())

    def agregar_producto_factura(self, ):
        """
            Function asociada para agregar un producto a la factura
        """
        producto_factura = ProductoFacturar()
        producto_factura.id_factura = self.codigo_factura.get()
        producto_factura.id = self.codigo.get()
        producto_factura.nombre = self.nombre.get()
        producto_factura.precio_venta = float(self.precio.get())
        producto_factura.cantidad = int(self.txt_cantidad.get())
        producto_factura.sub_total = str(producto_factura.calcular_subtotal())

        id = self.validar_producto_existente_factura(producto_factura.nombre)  # Valida si el producto esta
        # existente solo para aumentar su cantidad
        if id:
            self.factura.remover_producto(producto_factura.nombre)
            producto_facturar_edit = self.detalle_factura.item(id)
            producto_viejo_valores = producto_facturar_edit['values']
            producto_factura_cant_ant = int(producto_viejo_valores[0])
            self.detalle_factura.delete(id)
            nueva_cantidad = int(producto_factura.cantidad) + int(producto_factura_cant_ant)
            producto_factura.cantidad = nueva_cantidad
            producto_factura.sub_total = str(producto_factura.calcular_subtotal())
            self.detalle_factura.insert('', 0, text=producto_factura.nombre, values=(
                producto_factura.cantidad, producto_factura.precio_venta, producto_factura.sub_total), iid=id)

        else:
            self.detalle_factura.insert('', 0, text=producto_factura.nombre, values=(
                producto_factura.cantidad, producto_factura.precio_venta, producto_factura.sub_total)
                                        )
        self.factura.lista_productos.append(producto_factura)

        self.producto_factura.destroy()

        self.total.set(float(self.factura.calcular_total()))

    def mostrar_sub_total(self, event):
        # Calcula el subtotal del un producto y lo muestra
        sub_total = float(self.precio.get()) * int(self.txt_cantidad.get())
        self.sub_total.set(str(sub_total))

    def widget_agregar_producto_factura(self, event):
        """
         Ventana hija asociada al momento de selecionar
         un producto y muestra su informacion y la cantidad
         de producto requerida
        """
        id = self.listdetalle.focus()
        producto_focus = self.listdetalle.item(id)
        lista = []
        for atributos in producto_focus['values']:
            lista.append(atributos)

        self.producto_factura = Toplevel()
        self.producto_factura.title("SYST_CONTROL(REST®)--›(Añadir a Factura)")
        self.producto_factura.geometry('460x250')
        self.producto_factura.iconbitmap('recursos\\icon_rest.ico')
        self.producto_factura.configure(bg='#a27114')
        self.producto_factura.transient(master=self.root)
        self.producto_factura.wait_visibility()
        self.producto_factura.grab_set()

        # Widgets para añadir un producto
        self.label_imp_fac = LabelFrame(self.producto_factura, width=430, height=220, bg='#a27114')
        self.label_imp_fac.place(x=15, y=15)

        self.lb_cod_producto = Label(self.label_imp_fac, text='CÓD.                          :',
                                     font=('Copperplate Gothic Bold', 10), width=13, bg='#808080')
        self.lb_cod_producto.place(x=15, y=15)

        self.codigo = StringVar()
        self.tx_codigo = Entry(self.label_imp_fac, state='readonly', textvariable=self.codigo,
                               width=10).place(x=150, y=15)
        self.codigo.set(producto_focus['text'])

        self.lb_nb_producto = Label(self.label_imp_fac, text='DESCRIPCIÓN    :', font=('Copperplate Gothic Bold', 10),
                                    width=13, bg='#808080')
        self.lb_nb_producto.place(x=15, y=45)

        self.nombre = StringVar()
        self.txt_nb_producto = Entry(self.label_imp_fac, state='readonly', textvariable=self.nombre,
                                     width=40).place(x=150, y=45)
        self.nombre.set(lista[0])

        self.lb_precio = Label(self.label_imp_fac, text='PRECIO                $:',
                               font=('Copperplate Gothic Bold', 10),
                               width=13, bg='#808080')
        self.lb_precio.place(x=15, y=75)

        self.precio = StringVar()
        self.txt_precio = Entry(self.label_imp_fac, state='readonly', textvariable=self.precio,
                                width=5).place(x=150, y=75)
        self.precio.set(lista[1])

        self.lb_cantidad = Label(self.label_imp_fac, text='CANTIDAD           :', font=('Copperplate Gothic Bold', 10),
                                 width=13, bg='#808080')
        self.lb_cantidad.place(x=15, y=105)
        self.cantidad = StringVar()
        self.cantidad.set('1')
        self.txt_cantidad = Entry(self.label_imp_fac, textvariable=self.cantidad, validate='key', width=5,
                                  validatecommand=(self.validatecommand, "%S"))
        self.txt_cantidad.focus()
        self.txt_cantidad.bind('<Return>', self.mostrar_sub_total)
        self.txt_cantidad.place(x=150, y=105)

        self.lb_sub_total = Label(self.label_imp_fac, text=' SUBTOTAL       $:', font=('Copperplate Gothic Bold', 10),
                                  width=13, bg='#808080')
        self.lb_sub_total.place(x=15, y=135)

        self.sub_total = StringVar()
        self.txt_sub_total = Entry(self.label_imp_fac, state='readonly', textvariable=self.sub_total, width=5)
        self.txt_sub_total.place(x=150, y=135)

        self.btAdd = Button(self.label_imp_fac, image=self.imagenes['reportes'], text=' AÑADIR A FACTURA ',
                            width=160, command=self.agregar_producto_factura, compound=RIGHT)
        self.btAdd.image = self.imagenes['reportes']
        self.btAdd.place(x=150, y=170)

    def crear_o_editar_producto(self, op):
        """
        Funcion asociada para crear o actualizar un producto
        """
        if self.txtCodigo.get() == '':
            messagebox.showerror("SYST_CONTROL(REST®)-->(ERROR)", "POR FAVOR INGRESE EL CAMPO: Cód. DE PRODUCTO")
            self.txtCodigo.focus()

        elif self.txtNombre.get() == '':
            messagebox.showerror("SYST_CONTROL(REST®)-->(ERROR)", "POR FAVOR INGRESE EL CAMPO: DESCRIPCIÓN DE PRODUCTO")
            self.txtNombre.focus()

        elif self.txtPrecio_compra.get() == '':
            messagebox.showerror("SYST_CONTROL(REST®)-->(ERROR)", "POR FAVOR INGRESE EL CAMPO: PRECIO DE COMPRA "
                                                                  "DE PRODUCTO")
            self.txtPrecio_compra.focus()

        elif self.txtPrecio_venta.get() == '':
            messagebox.showerror("SYST_CONTROL(REST®)-->(ERROR)", "POR FAVOR INGRESE EL CAMPO: PRECIO DE VENTA "
                                                                  "DE PRODUCTO")
            self.txtPrecio_venta.focus()

        elif self.txtStock.get() == '':
            messagebox.showerror("SYST_CONTROL(REST®)-->(ERROR)", "POR FAVOR INGRESE EL CAMPO: STOCK DE PRODUCTO")
            self.txtStock.focus()

        elif self.valor.get() == '':
            messagebox.showerror("SYST_CONTROL(REST®)-->(ERROR)", "POR FAVOR INGRESE EL CAMPO: ESTADO DE PRODUCTO")
            self.txtStock.focus()

        else:
            producto = Producto()

            producto.id = self.txtCodigo.get()
            producto.nombre = self.txtNombre.get()
            producto.precio_compra = float(self.txtPrecio_compra.get())
            producto.precio_venta = float(self.txtPrecio_venta.get())
            producto.stock = int(self.txtStock.get())
            producto.estado = self.valor.get()

            if producto.validar():  # Valida si el objeto tiene valores nulos
                if op == 1:  # Parametro recibido del boton nuevo
                    if producto.guardar():
                        self.listar_productos()
                        self.nuevo_producto.destroy()
                elif op == 2:  # Parametro recibido del boton actualizar
                    if producto.actualizar():
                        self.nuevo_producto.destroy()
                        self.listar_productos()

            else:
                messagebox.showerror("SYST_CONTROL(REST®)-->(ERROR)", "POR FAVOR INGRESE NUEVAMENTE EL PRODUCTO")

    def actualizar_producto(self):
        """
            Funcion para actualizar un producto
        """

        producto = Producto()
        producto.id = self.txtCodigoED.get()  # Recibe el id de producto

        producto_editar = producto.seleccionar()  # SQL que devuelve el producto escogido

        if producto_editar:
            self.VtBuscar.destroy()

            for producto_edit in producto_editar:  # Llena la ventana con los datos del producto
                self.widgets_producto()
                self.nuevo_producto.title('Editar producto')
                self.txtCodigo.insert(0, producto_edit[0])
                self.txtNombre.insert(0, producto_edit[1])
                self.txtPrecio_compra['validate'] = 'none'
                self.txtPrecio_venta['validate'] = 'none'

                self.txtPrecio_compra.insert(END, float(producto_edit[2]))
                self.txtPrecio_compra['validate'] = 'key'
                self.txtPrecio_venta.insert(END, float(producto_edit[3]))
                self.txtPrecio_compra['validate'] = 'key'
                self.txtStock.insert(0, (producto_edit[4]))
                self.valor.set(producto_edit[5])

                self.BtnGuardar['command'] = lambda: self.crear_o_editar_producto(2)

    def inactivar_producto(self):
        # Inactiva un producto para que no se liste
        id = self.listdetalle.focus()
        elementos = self.listdetalle.item(id)
        producto = Producto()
        producto.id = elementos['text']
        producto.estado = False

        if producto.inactivar():
            self.listar_productos()

    def listar_productos(self):
        # Lista todos los productos activos

        consulta = 'SELECT * FROM INV_PRODUCTO WHERE estado=1 AND inventario >0'
        productos_qs = conexion_consulta(consulta, parametros=())
        p = productos_qs
        self.llenar_registros(p)  # Ver linea 514

    def llenar_registros(self, p):
        # Funcion que llena la ventana productos con el sql listar producto
        registros = self.listdetalle.get_children()
        productos_qs = p
        for items in registros:
            self.listdetalle.delete(items)

        for element in productos_qs:
            self.listdetalle.insert('', 0, text=element[0], values=(element[1],
                                                                    element[3],
                                                                    element[4],
                                                                    )
                                    )
        self.listdetalle.bind('<Double-1>', self.widget_agregar_producto_factura)  # Evento que permite que se abra
        # la ventana para añadir a la factura

    def nueva_factura(self):
        # Limpiar productos en facturas
        self.widget_facturacion()
        id_detalle = self.detalle_factura.get_children()
        for item in id_detalle:
            self.detalle_factura.delete(item)

        self.total.set(0.00)
        self.tipo_moneda.current(0)
        self.cambio.set(0.00)
        self.txt_pago.delete(0, END)

    def validar_producto_existente_factura(self, nombre):
        """
            Funcion que verifica si un producto esta añadido a la factura
            Si el caso es verdadero la cantidad solo se actualiza
        """
        lista_producto = self.detalle_factura.get_children()

        for productos in lista_producto[::-1]:
            producto_agregado = self.detalle_factura.item(productos)
            if nombre == producto_agregado['text']:
                return productos
            else:
                return False

    def calcular_cambio(self, event):
        if self.txt_pago.get() >= self.total.get():
            # Calcula el cambio
            billete = float(self.txt_pago.get())
            cambio = billete - float(self.total.get())
            self.cambio.set(str(cambio))

        else:
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "EL TOTAL DE LA FACTURA EXCEDE EL "
                                                                          "VALOR DE PAGO!!!")
            self.pago_f.set(0.00)
            self.cambio.set("")
            self.txt_pago.focus()

    def obtener_clientes(self):
        a = self.search_field.get()
        if self.search_field.get() == "":
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: No. CÉDULA!!!")
            self.cliente.focus()

        elif a.isalpha():
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "NO SE ADMITEN LETRAS EN EL CAMPO DE "
                                                                          "BÚSQUEDA")
            self.search_field.set("")
            self.cliente.focus()

        elif a.isspace():
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "NO SE PERMITEN ESPACIOS EN EL CAMPO DE "
                                                                          "BÚSQUEDA!!!")
            self.search_field.set("")
            self.cliente.focus()

        else:
            if len(a) == 10:
                self.n_c_cl = self.search_field.get()

                try:
                    # Lista todos los cliente y lo muestra en el combobox de factura
                    consulta = 'SELECT * FROM INV_CLIENTE '
                    data = conexion_consulta(consulta, parametros=())
                    if data != "":
                        consulta = 'SELECT * FROM INV_CLIENTE '
                        data1 = conexion_consulta(consulta, parametros=())
                        for values1 in data1:
                            data_list_n = str(values1[1])
                            data_list_d = str(values1[2])
                            self.nombres_al.set(data_list_n)
                            self.direcccion_al.set(data_list_d)

                except BaseException as msg:
                    messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", F"No. DE CÉDULA NO VÁLIDO!!!\n"
                                                                                  F"INGRESE NUEVAMENTE {msg}")
                    self.search_field.set("")
                    self.nombres_al.set("")
                    self.direcccion_al.set("")
                    self.cliente.focus()

    def guardar_factura(self):
        """Guarda el registro de la factura"""
        if self.txt_pago != '':  # Si el pago no esta vacio
            factura = self.factura

            for productos_factura in self.factura.lista_productos:
                productos_factura.guardar()

            factura.id_factura = self.codigo_factura.get()
            id_cliente = self.cliente.get()
            lista_cliente = id_cliente.split('_')
            factura.id_cliente = lista_cliente[0]
            factura.nom_ape_cl = self.name_e.get()
            factura.dir_cl = self.dir_e_al.get()
            fecha = datetime.now()
            factura.fecha_creacion = '{}-{}-{}'.format(fecha.day, fecha.month, fecha.year)
            factura.hora_creacionW = '{}:{}'.format(fecha.hour, fecha.day)
            factura.pago = self.txt_pago.get()
            factura.cambio = self.cambio.get()
            recibo = ReciboFactura()  # Instancia del recibo factura
            recibo.detalles_factura(factura)  # se pasa el objeto para ser llenado el recibo
            recibo.save()

            recibo.__del__()

            factura.guardar()
            factura.lista_productos.clear()
            self.nueva_factura()
            self.listar_productos()

        else:
            pass

    def widget_cliente(self):
        self.ventana = Toplevel()
        self.ventana.title("SYST_CONTROL(REST®)--›(Nuevo cliente)")
        self.ventana.geometry('450x180')
        self.ventana.iconbitmap('recursos\\icon_rest.ico')
        self.ventana.wait_visibility()
        self.ventana.grab_set()
        self.ventana.transient(master=self.root)

        # Manage Frame
        self.Manage_Frame_c = Frame(self.ventana, relief=RIDGE, bd=4, bg='#a27114')
        self.Manage_Frame_c.place(x=0, y=0, width=450, height=180)

        # Widgets para añadir un cliente
        self.lbnumced = Label(self.Manage_Frame_c, text='No. CÉDULA   :', font=("Copperplate Gothic Bold", 10, "bold"),
                              bg='#a27114', fg="White")
        self.lbnumced.place(x=10, y=10)
        self.txt_codigo_1 = StringVar()
        self.txt_codigo = Entry(self.Manage_Frame_c, textvariable=self.txt_codigo_1, width=10)
        self.txt_codigo.place(x=128, y=10)

        self.lbl_nombre = Label(self.Manage_Frame_c, text='NOMBRES       :', font=("Copperplate Gothic Bold", 10, "bold"),
                                bg='#a27114', fg="White")
        self.lbl_nombre.place(x=10, y=40)
        self.txt_nombre = Entry(self.Manage_Frame_c, width=40)
        self.txt_nombre.place(x=128, y=40)

        self.lbl_n_celular = Label(self.Manage_Frame_c, text='No. CELULAR:',
                                   font=("Copperplate Gothic Bold", 10, "bold"), bg='#a27114', fg="White")
        self.lbl_n_celular.place(x=10, y=70)
        self.txt_n_celular = Entry(self.Manage_Frame_c, width=40)
        self.txt_n_celular.place(x=128, y=70)

        self.lbl_direccion = Label(self.Manage_Frame_c, text='DIRECCIÓN    :',
                                   font=("Copperplate Gothic Bold", 10, "bold"),
                                   bg='#a27114', fg="White")
        self.lbl_direccion.place(x=10, y=100)
        self.txt_direccion = Entry(self.Manage_Frame_c, width=50)
        self.txt_direccion.place(x=128, y=100)

        self.btn_guardar = Button(self.Manage_Frame_c, image=self.imagenes['nuevo'], text='GUARDAR', width=80,
                                  command=self.guardar_cliente, compound="right")
        self.btn_guardar.image = self.imagenes['nuevo']
        self.btn_guardar.place(x=175, y=130)

    def guardar_cliente(self):
        if self.txt_codigo_1.get() == "":
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: No. CÉDULA!!!")
            self.txt_codigo_1.set("")
            self.txt_codigo.focus()

        elif self.txt_nombre.get() == "":
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: NOMBRES")

            self.txt_nombre.focus()

        elif self.txt_n_celular.get() == "":
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: No. CELULAR")

            self.txt_n_celular.focus()

        elif self.txt_direccion.get() == "":
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: DIRECCIÓN")
            self.txt_direccion.focus()

        else:
            a = self.txt_codigo_1.get()
            if a.isalpha():
                messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "NO SE ADMITEN LETRAS EN EL CAMPO: "
                                                                              "No. CÉDULA")
                self.txt_codigo_1.set("")
                self.txt_codigo.focus()

            elif a.isspace():
                messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "NO SE PERMITEN ESPACIOS EN EL CAMPO: "
                                                                              "No. CÉDULA")
                self.txt_codigo_1.set("")
                self.txt_codigo.focus()

            elif len(a) != 10:
                messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "No. CÉDULA NO VÁLIDO")
                self.txt_codigo_1.set("")
                self.txt_codigo.focus()

            else:
                # Guarda un cliente
                cliente = Cliente()
                cliente.id = self.txt_codigo.get()
                cliente.nombre = self.txt_nombre.get()
                cliente.n_celular = self.txt_n_celular.get()
                cliente.direccion = self.txt_direccion.get()

                cliente.guardar()
                self.ventana.destroy()

    def logout(self):
        root = Toplevel()
        login_form.Login(root)
        self.root.withdraw()
        root.deiconify()

    def principal_btn(self):
        root = Toplevel()
        Principal_Window_C.Principal_C(root)
        self.root.withdraw()
        root.deiconify()

    def ver_fct_btn(self):
        root = Toplevel()
        Re_Facturation_F.Ventana_Principal_1(root)
        self.root.withdraw()
        root.deiconify()

    def pass_btn(self):
        root = Toplevel()
        Password_Window_C.Password(root)
        self.root.withdraw()
        root.deiconify()

    def salir_principal(self):
        self.sa = messagebox.askyesno('SIST_CONTROL (REST®) CERRAR SESIÓN', 'CERRAR SYST_CONTROL(REST®)')
        if self.sa:
            raise SystemExit

        # =============================================================
        # FUNCIÓN CAJA DE INFORMACIÓN DEL SISTEMA(INFO)
        # =============================================================

    def caja_info_sist(self):
        self.men2 = messagebox.showinfo('SIST_CONTROL (REST®)',
                                        'SIST_CONTROL (REST®) v1.0\n'
                                        'El uso de este software queda sujeto a los términos y condiciones del '
                                        'contrato "J.C.F DESING®-CLIENTE".    \n'
                                        'El uso de este software queda sujeto a su contrato. No podrá utilizar '
                                        'este software para fines de distribución\n'
                                        'total o parcial.\n\n\n© 2022 J.C.F DESING®. Todos los derechos reservados')


def root():
    root = tk.ThemedTk()
    root.get_themes()
    root.set_theme("arc")
    Facturation(root)
    root.mainloop()


if __name__ == '__main__':
    root()

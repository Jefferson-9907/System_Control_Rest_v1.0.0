import random
from time import strftime
from tkinter import *
from tkinter import messagebox
from ttkthemes import themed_tk as tk
from tkinter.ttk import Treeview, Combobox
from datetime import datetime

import login_form
import Principal_Window_A
import Re_Facturation
import Report_Window_A
import Password_Window_A
import Users_Window_A
import Materia_Prima_Window_A
import Producto_Window_A
import Proveedor_Window_A
from modelos import Producto, ProductoFacturar, Factura, Cliente
from funciones_auxiliares import solo_numero, conexion_consulta
from reportes import ReciboFactura


class Facturation:
    """
        Contiene todos los widgets necesario para la facturacion
    """

    def __init__(self, root):

        self.root = root
        self.root.title("SYST_CONTROL--›Facturación")
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.iconbitmap('recursos\\icon_principal.ico')
        self.root.configure(bg='#a27114')

        self.imagenes = {
            'nuevo': PhotoImage(file='recursos\\icon_add.png'),
            'editar': PhotoImage(file='recursos\\icon_update.png'),
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
        # CREACIÓN DEL MENÚ
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
        # AÑADIENDO OPCIÓN: INVENTARIO AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='INVENTARIO', menu=self.Column2)
        self.Column2.add_command(label='Materia Prima', command=self.materia_prima_btn)
        self.Column2.add_command(label='Platos', command=self.producto_btn)
        self.Column3 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: COMPRA AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='COMPRA', menu=self.Column3)
        self.Column3.add_command(label='Proveedor_W', command=self.proveedor_btn)
        self.Column3.add_command(label='Materia Prima', command=self.materia_prima_btn)
        self.Column4 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: VENTA AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='VENTA', menu=self.Column4)
        self.Column4.add_command(label='Tíket')
        self.Column4.add_command(label='Verificar Tíket')
        self.Column5 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: CAJA AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='CAJA', menu=self.Column5)
        self.Column5.add_command(label='Apertura')
        self.Column6 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: CUENTAS AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='CUENTAS', menu=self.Column6)
        self.Column6.add_command(label='Por Pagar')
        self.Column6.add_command(label='Por Cobrar')
        self.Column7 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: REPORTES AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='REPORTES', menu=self.Column7)
        self.Column7.add_command(label='Generar Reportes')
        self.Column8 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: USUARIOS AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='USUARIOS', menu=self.Column8)
        self.Column8.add_command(label='Cambiar Usuario', command=self.logout)
        self.Column8.add_command(label='Cambiar Contraseña', command=self.pass_btn)
        self.Column8.add_command(label='Usuarios', command=self.users_btn)
        self.Column8.add_separator()
        self.Column8.add_command(label='Cerrar Sesión', command=self.salir_principal)
        self.Column8.add_separator()
        self.Column9 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: INFO AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='INFO', menu=self.Column9)
        self.Column9.add_command(label='Sobre SIST_CONTROL (REST®)', command=self.caja_info_sist)
        self.Column9.add_separator()
        self.root.config(menu=self.menus)

        self.footer_4 = Label(self.root, text='J.C.F DESING® | Derechos Reservados 2021', width=195, bg='black',
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
        self.ventana_productos()  # Seccion
        """self.widget_menu_inferior()"""
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
            Botones asociados en la barra superior acerca del estado de los productos
        """
        self.label_producto = LabelFrame(self.root, text='Opciones del inventario', bg='#a27114', width=520, height=90)
        self.label_producto.place(x=15, y=80)

        self.Btnproducto = Button(self.label_producto, image=self.imagenes['nuevo'], text='Nuevo',
                                  command=self.widgets_producto, compound=TOP)
        self.Btnproducto.image = self.imagenes['nuevo']
        self.Btnproducto.place(x=15, y=5)

        self.Btneditar = Button(self.label_producto, image=self.imagenes['editar'], command=self.widget_buscar_producto,
                                text='Editar', compound=TOP)
        self.Btneditar.image = self.imagenes['editar']
        self.Btneditar.place(x=75, y=5)

        self.Btninactivar = Button(self.label_producto, image=self.imagenes['inactivar'],
                                   command=self.inactivar_producto, text='Inactivar', compound=TOP)
        self.Btninactivar.image = self.imagenes['inactivar']
        self.Btninactivar.place(x=139, y=5)

        self.Btnactualizar = Button(self.label_producto, image=self.imagenes['actualizar'], command=self.principal_btn,
                                    text='Refrescar', compound=TOP)
        self.Btnactualizar.image = self.imagenes['actualizar']
        self.Btnactualizar.place(x=223, y=5)

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

        self.labelframe_buscador = LabelFrame(self.root, text="Buscar Implemento", bg='#a27114', width=520, height=60)
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
            Funcion asociada a widget buscar para la busqueda de un producto
        """
        b = self.busc.get()

        if self.txtBuscar.get() == "":
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL NOMBRE DEL IMPLEMENTO EN EL "
                                                                          "CAMPO DE BÚSQUEDA!!!")
            self.busc.set("")
            self.txtBuscar.focus()

        elif b.isnumeric():
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "NO SE ADMITEN LETRAS EN EL CAMPO DE "
                                                                          "BÚSQUEDA")
            self.busc.set("")
            self.txtBuscar.focus()

        elif b.isspace():
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "NO SE PERMITEN ESPACIOS EN EL CAMPO DE "
                                                                          "BÚSQUEDA!!!")
            self.busc.set("")
            self.txtBuscar.focus()

        else:
            varia = str(self.txtBuscar.get())
            consulta = "SELECT * FROM producto WHERE nombre LIKE '%' || ? ||'%'"
            parametros = [varia]

            producto_qs = conexion_consulta(consulta, parametros)

            if producto_qs.fetchone():
                p = producto_qs
                self.llenar_registros(p)
                self.busc.set("")
            else:
                messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)",
                                       f"NO SE ENCONTARON IMPLEMENTOS CON DESCRIPCIÓN: {self.txtBuscar.get()}!!!")
                self.busc.set("")
                self.txtBuscar.focus()

    def ventana_productos(self):
        """
            Widget que muestra los productos en general o ya filtrado en una busqueda
        """
        self.labelproductos = LabelFrame(self.root, width=520, height=448, text='Listado Implementos', bg='#a27114')
        self.labelproductos.place(x=15, y=240)
        self.listdetalle = Treeview(self.labelproductos, columns=('#0', '#1', '#2'), height=17)

        self.listdetalle.column('#0', width=50)
        self.listdetalle.column('#1', width=315)
        self.listdetalle.column('#2', width=50)
        self.listdetalle.column('#3', width=50)

        self.listdetalle.heading('#0', text='ID')
        self.listdetalle.heading('#1', text='Implemento ')
        self.listdetalle.heading('#2', text='Precio')
        self.listdetalle.heading('#3', text='Stock')

        self.listdetalle.place(x=10, y=10)

    def widget_buscar_producto(self):
        """
         Ventana hija para buscar un producto y actualizarlo
        """
        self.VtBuscar = Toplevel()
        self.VtBuscar.title('SYST_CONTROL--›Editar u Eliminar')
        self.VtBuscar.geometry('510x90')
        self.VtBuscar.iconbitmap('recursos\\ICONO_SIST_CONTROL (IFAP®)2.0.ico')
        self.VtBuscar.configure(bg='#a27114')
        self.VtBuscar.transient(master=self.root)
        self.VtBuscar.grab_set()

        self.label_impl = LabelFrame(self.VtBuscar, width=480, height=60, bg='#a27114')
        self.label_impl.place(x=15, y=15)

        self.lbCodigoED = Label(self.label_impl, text='CÓD. IMPLEMENTO', font=('Copperplate Gothic Bold', 10), width=17,
                                bg='#808080')
        self.lbCodigoED.place(x=15, y=15)

        self.impl_f = StringVar()
        self.txtCodigoED = Entry(self.label_impl, textvariable=self.impl_f, width=30)
        self.txtCodigoED.focus()
        self.txtCodigoED.place(x=190, y=15)

        self.btnED = Button(self.label_impl, image=self.imagenes['buscar'], text=' BUSCAR ',
                            command=self.actualizar_producto, compound=LEFT)
        self.btnED.image = self.imagenes['buscar']
        self.btnED.place(x=380, y=10)

    def widgets_producto(self):
        """
            Ventana hija asociada al boton nuevo que funciona para agregar o modifcar un producto
        """
        self.nuevo_producto = Toplevel()
        self.nuevo_producto.title('SYST_CONTROL--›Nuevo Implemento')
        self.nuevo_producto.geometry('490x275')
        self.nuevo_producto.iconbitmap('recursos\\ICONO_SIST_CONTROL (IFAP®)2.0.ico')
        self.nuevo_producto.configure(bg='#a27114')
        self.nuevo_producto.transient(master=self.root)
        self.nuevo_producto.grab_set()

        # Widgets para añadir un producto
        self.label_n_impl = LabelFrame(self.nuevo_producto, width=460, height=245, bg='#a27114')
        self.label_n_impl.place(x=15, y=15)

        self.lbCodigo = Label(self.label_n_impl, text='CÓD.               ', font=('Copperplate Gothic Bold', 10),
                              width=15, bg='#808080')
        self.lbCodigo.place(x=15, y=15)
        self.txtCodigo = Entry(self.label_n_impl, width=5)
        self.txtCodigo.focus()
        self.txtCodigo.place(x=165, y=15)

        self.lbNombre = Label(self.label_n_impl, text=' DESCRIPCIÓN', font=('Copperplate Gothic Bold', 10), width=15,
                              bg='#808080')
        self.lbNombre.place(x=15, y=45)
        self.txtNombre = Entry(self.label_n_impl, width=45)
        self.txtNombre.place(x=165, y=45)

        self.lbPrecio_compra = Label(self.label_n_impl, text=' PRECIO COMPRA $',
                                     font=('Copperplate Gothic Bold', 10), width=15, bg='#808080')
        self.lbPrecio_compra.place(x=15, y=75)
        self.txtPrecio_compra = Entry(self.label_n_impl, width=5, validate='key',
                                      validatecommand=(self.validatecommand, "%S"))
        self.txtPrecio_compra.place(x=165, y=75)

        self.lbPrecio_venta = Label(self.label_n_impl, text=' PRECIO VENTA $', font=('Copperplate Gothic Bold', 10),
                                    width=15, bg='#808080')
        self.lbPrecio_venta.place(x=15, y=105)
        self.txtPrecio_venta = Entry(self.label_n_impl, width=5, validate='key',
                                     validatecommand=(self.validatecommand, "%S"))
        self.txtPrecio_venta.place(x=165, y=105)

        self.lbStock = Label(self.label_n_impl, text=' INVENTARIO ', font=('Copperplate Gothic Bold', 10), width=15,
                             bg='#808080')
        self.lbStock.place(x=15, y=135)
        self.txtStock = Entry(self.label_n_impl, width=5, validate='key',
                              validatecommand=(self.validatecommand, "%S"))
        self.txtStock.place(x=165, y=135)

        self.estado = Label(self.label_n_impl, text=' DISPONIBLE ', font=('Copperplate Gothic Bold', 10), width=15,
                            bg='#808080')
        self.estado.place(x=15, y=165)
        self.valor = BooleanVar()
        self.txtEstado = Checkbutton(self.label_n_impl, variable=self.valor, onvalue=True, offvalue=False)
        self.txtEstado.place(x=165, y=165)

        # Botones
        self.BtnGuardar = Button(self.label_n_impl, image=self.imagenes['nuevo'], text=' GUARDAR ',
                                 command=lambda: self.crear_o_editar_producto(1), compound=LEFT)
        self.BtnGuardar.image = self.imagenes['nuevo']
        self.BtnGuardar.place(x=200, y=200)

    def widget_facturacion(self):
        """
             Ventana que asocia todos los controles e informacion
             acerca de la facturacion de un producto, no disponible cuando
             inicia, para acceder a ella presionar el boton nueva venta
        """
        self.label_facturacion = LabelFrame(self.root, width=800, height=605, bg='#a27114')
        self.label_facturacion.place(x=550, y=85)

        self.lb_cod_factura = Label(self.label_facturacion, text='CÓD. FACTURA', bg='#a27114', fg="White",
                                    font=("Copperplate Gothic Bold", 12, "bold"))
        self.lb_cod_factura.place(x=420, y=10)

        self.codigo_factura = StringVar()
        self.txt_cod_factura = Entry(self.label_facturacion, state='readonly', textvariable=self.codigo_factura,
                                     fg='Red', width=14, font=('Copperplate Gothic Bold', 14), relief=RIDGE)
        self.txt_cod_factura.place(x=580, y=10)

        self.label_facturacion_1 = LabelFrame(self.root, text='Datos para factura', width=760, height=100,
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
        self.name_e.place(x=110, y=40)

        self.lb_direccion = Label(self.label_facturacion_1, text='DIRECCIÓN', font=('Copperplate Gothic Bold', 10),
                                  bg='#808080', width=10)
        self.lb_direccion.place(x=390, y=40)
        self.direcccion_al = StringVar()
        self.dir_e_al = Entry(self.label_facturacion_1, width=40, textvariable=self.direcccion_al, state='readonly')
        self.dir_e_al.place(x=490, y=40)

        self.lb_detalle = Label(self.label_facturacion, text='-------DETALLE FACTURA-------', bg='#a27114', fg="White",
                                font=("Copperplate Gothic Bold", 16, "bold"))
        self.lb_detalle.place(x=245, y=160)

        self.detalle_factura = Treeview(self.label_facturacion, columns=('#0', '#1', '#2',), height=10)
        self.detalle_factura.place(x=20, y=200)
        self.detalle_factura.column('#0', width=500)
        self.detalle_factura.column('#1', width=75)
        self.detalle_factura.column('#2', width=75)
        self.detalle_factura.column('#3', width=75)

        self.detalle_factura.heading('#0', text='Implemento')
        self.detalle_factura.heading('#1', text='Cant.')
        self.detalle_factura.heading('#2', text='Precio')
        self.detalle_factura.heading('#3', text='Subtotal')

        self.total = StringVar()
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

        self.BtnFacturar = Button(self.label_facturacion, image=self.imagenes['print'], text='FACTURAR', width=80,
                                  command=self.guardar_factura, compound=TOP)
        self.BtnFacturar.image = self.imagenes['print']
        self.BtnFacturar.place(x=490, y=505)

    def agregar_producto_factura(self, ):
        """
            Funcion asociada para agregar un producto a la factura
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

        self.total.set(str(self.factura.calcular_total()))

    def mostrar_sub_total(self, event):
        # Calcula el subtotal del un producto y lo muestra
        sub_total = float(self.precio.get()) * int(self.txt_cantidad.get())
        self.sub_total.set(str(sub_total))

    def widget_agregar_producto_factura(self, event):
        """
         Ventana hija asociada al momento de selecionar un producto y muestra su informacion y la cantidad
         de producto requerida
        """
        id = self.listdetalle.focus()
        producto_focus = self.listdetalle.item(id)
        lista = []
        for atributos in producto_focus['values']:
            lista.append(atributos)

        self.producto_factura = Toplevel()
        self.producto_factura.title('SYST_CONTROL--›Añadir a Factura')
        self.producto_factura.geometry('460x250')
        self.producto_factura.iconbitmap('recursos\\ICONO_SIST_CONTROL (IFAP®)2.0.ico')
        self.producto_factura.configure(bg='#a27114')
        self.producto_factura.transient(master=self.root)
        self.producto_factura.wait_visibility()
        self.producto_factura.grab_set()

        # Widgets para añadir un producto
        self.label_imp_fac = LabelFrame(self.producto_factura, width=430, height=220, bg='#a27114')
        self.label_imp_fac.place(x=15, y=15)

        self.lb_cod_producto = Label(self.label_imp_fac, text='CÓD.               ',
                                     font=('Copperplate Gothic Bold', 10), width=13, bg='#808080')
        self.lb_cod_producto.place(x=15, y=15)

        self.codigo = StringVar()
        self.tx_codigo = Entry(self.label_imp_fac, state='readonly', textvariable=self.codigo,
                               width=5).place(x=150, y=15)
        self.codigo.set(producto_focus['text'])

        self.lb_nb_producto = Label(self.label_imp_fac, text=' DESCRIPCIÓN ', font=('Copperplate Gothic Bold', 10),
                                    width=13, bg='#808080')
        self.lb_nb_producto.place(x=15, y=45)

        self.nombre = StringVar()
        self.txt_nb_producto = Entry(self.label_imp_fac, state='readonly', textvariable=self.nombre,
                                     width=40).place(x=150, y=45)
        self.nombre.set(lista[0])

        self.lb_precio = Label(self.label_imp_fac, text='PRECIO          $', font=('Copperplate Gothic Bold', 10),
                               width=13, bg='#808080')
        self.lb_precio.place(x=15, y=75)

        self.precio = StringVar()
        self.txt_precio = Entry(self.label_imp_fac, state='readonly', textvariable=self.precio,
                                width=5).place(x=150, y=75)
        self.precio.set(lista[1])

        self.lb_cantidad = Label(self.label_imp_fac, text='CANTIDAD    ', font=('Copperplate Gothic Bold', 10),
                                 width=13, bg='#808080')
        self.lb_cantidad.place(x=15, y=105)
        self.cantidad = StringVar()
        self.cantidad.set('1')
        self.txt_cantidad = Entry(self.label_imp_fac, textvariable=self.cantidad, validate='key', width=5,
                                  validatecommand=(self.validatecommand, "%S"))
        self.txt_cantidad.focus()
        self.txt_cantidad.bind('<Return>', self.mostrar_sub_total)
        self.txt_cantidad.place(x=150, y=105)

        self.lb_sub_total = Label(self.label_imp_fac, text=' SUBTOTAL        $', font=('Copperplate Gothic Bold', 10),
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
        if self.txtCodigo.get() == "" or self.txtNombre.get() == "" or self.txtPrecio_compra.get() == "" or \
                self.txtPrecio_venta.get() == "" or self.txtStock.get() == "":
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "TODOS LOS CAMPOS SON OBLIGATORIOS!!!")

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
                messagebox.showerror("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "TODOS LOS CAMPOS SON OBLIGATORIOS!!!")

    def actualizar_producto(self):
        """
            Funcion para actualizar un producto
        """
        if self.txtCodigoED.get() == "":
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: CÓD. IMPLEMENTO!!!")
            self.txtCodigoED.focus()

        else:
            a = self.txtCodigoED.get()
            if self.txtCodigoED.get() == "":
                messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: CÓD. IMPLEMENTO!!!")
                self.impl_f.set("")
                self.txtCodigoED.focus()

            elif a.isalpha():
                messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "NO SE ADMITEN LETRAS EN EL CAMPO DE "
                                                                              "BÚSQUEDA")
                self.impl_f.set("")
                self.txtCodigoED.focus()

            elif a.isspace():
                messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "NO SE PERMITEN ESPACIOS EN EL CAMPO DE "
                                                                              "BÚSQUEDA!!!")
                self.impl_f.set("")
                self.txtCodigoED.focus()

            else:
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
        consulta = 'SELECT * FROM producto WHERE estado=1 AND inventario >0'
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
            self.busc.set("")
        self.listdetalle.bind('<Double-1>', self.widget_agregar_producto_factura)  # Evento que permite que se abra
        # la ventana para añadir a la factura

    def nueva_factura(self):
        # Limpiar productos en facturas
        self.widget_facturacion()
        id_detalle = self.detalle_factura.get_children()
        for item in id_detalle:
            self.detalle_factura.delete(item)

        self.total.set('')
        self.tipo_moneda.current(0)
        self.cambio.set('')
        self.txt_pago.delete(0, END)

        nuevo_codigo_fact = self.factura.obtener_numero_factura()
        self.codigo_factura.set(nuevo_codigo_fact)

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
        if self.txt_pago.get() < self.total.get():
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "EL TOTAL DE LA FACTURA EXCEDE EL "
                                                                          "VALOR DE PAGO!!!")
            self.pago_f.set("")
            self.cambio.set("")
            self.txt_pago.focus()

        else:
            # Calcula el cambio
            billete = float(self.txt_pago.get())
            cambio = billete - float(self.total.get())
            self.cambio.set(str(cambio))

    def obtener_clientes(self):
        a = self.search_field.get()
        if self.search_field.get() == "":
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: No. CÉDULA!!!")
            self.cliente.focus()

        elif a.isalpha():
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "NO SE ADMITEN LETRAS EN EL CAMPO DE "
                                                                          "BÚSQUEDA")
            self.search_field.set("")
            self.cliente.focus()

        elif a.isspace():
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "NO SE PERMITEN ESPACIOS EN EL CAMPO DE "
                                                                          "BÚSQUEDA!!!")
            self.search_field.set("")
            self.cliente.focus()

        else:
            if len(a) == 10:
                self.n_c_cl = self.search_field.get()
                # Lista todos los cliente y lo muestra en el combobox de factura
                consulta = 'SELECT * FROM Cliente WHERE ID=?'
                parametros = [self.n_c_cl]
                data = conexion_consulta(consulta, parametros)
                if data.fetchone():
                    consulta1 = 'SELECT * FROM Cliente WHERE ID=?'
                    parametros = [self.n_c_cl]
                    data1 = conexion_consulta(consulta1, parametros)
                    for values in data1:
                        data_list_n = str(values[1])
                        data_list_d = str(values[2])
                        self.nombres_al.set(data_list_n)
                        self.direcccion_al.set(data_list_d)

                else:
                    messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", f"NO EXISTEN REGISTROS DE "
                                                                                  f"FACTURACIÓN CON EL No. DE CÉDULA: "
                                                                                  f"")
                    self.sa = messagebox.askyesno("SYST_CONTROL(IFAP®)-->(REGISTRO)", f"REGISTAR CLIENTE CON EL No. "
                                                                                      f"DE CÉDULA: {self.n_c_cl}")
                    self.search_field.set("")
                    self.nombres_al.set("")
                    self.direcccion_al.set("")
                    if self.sa:
                        self.widget_cliente()

            else:
                messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "No. DE CÉDULA NO VÁLIDO!!!\n"
                                                                              "INGRESE NUEVAMENTE")
                self.search_field.set("")
                self.nombres_al.set("")
                self.direcccion_al.set("")
                self.cliente.focus()

    def guardar_factura(self):
        """
            Guarda el registro de la factura
        """
        if self.search_field.get() == "":
            messagebox.showwarning("SYSTEM_CONTROL(IFAP®)-->(ADVERTENCIA)",
                                   "DEBE DE LLENAR DATOS DEL CLIENTE A LA FACTURA")
            self.cliente.focus()

        elif self.pago_f.get() == 0.00:
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "EL TOTAL DE LA FACTURA EXCEDE EL "
                                                                          "VALOR DE PAGO!!!")
            self.pago_f.set("")
            self.cambio.set("")
            self.txt_pago.focus()

        else:  # Si el pago no esta vacio
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
            factura.hora_creacion = '{}:{}'.format(fecha.hour, fecha.minute)
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

    def bloquear(self):
        # Oculta el panel de factura
        self.label_facturacion.place_forget()
        self.root.geometry('810x700')

    def widget_cliente(self):
        # Añade un nuevo cliente
        self.ventana = Toplevel()
        self.ventana.title('SYST_CONTROL--›Nuevo Cliente')
        self.ventana.geometry('545x200')
        self.ventana.iconbitmap('recursos\\ICONO_SIST_CONTROL (IFAP®)2.0.ico')
        self.ventana.configure(bg='#a27114')
        self.ventana.transient(master=self.root)
        self.ventana.grab_set()

        self.label_client = LabelFrame(self.ventana, width=515, height=170, bg='#a27114')
        self.label_client.place(x=15, y=15)

        lbl_codigo = Label(self.label_client, text=' No. CÉDULA ',
                           font=('Copperplate Gothic Bold', 10), width=15, bg='#808080')
        lbl_codigo.place(x=10, y=10)
        self.id_cliente = StringVar()
        self.txt_codigo = Entry(self.label_client, textvariable=self.id_cliente, width=15)
        self.txt_codigo.focus()
        self.txt_codigo.bind('<Return>', self.sig_entry)
        self.txt_codigo.place(x=160, y=10)

        lbl_nombre = Label(self.label_client, text=' NOMBRES ', font=('Copperplate Gothic Bold', 10),
                           width=15, bg='#808080')
        lbl_nombre.place(x=10, y=40)
        self.nombres_f = StringVar()
        self.txt_nombre = Entry(self.label_client, textvariable=self.nombres_f, width=40)
        self.txt_nombre.bind('<Return>', self.sig_entry1)
        self.txt_nombre.place(x=160, y=40)

        lbl_apellido = Label(self.label_client, text=' APELLIDOS ', font=('Copperplate Gothic Bold', 10),
                             width=15, bg='#808080')
        lbl_apellido.place(x=10, y=70)
        self.apellidos_f = StringVar()
        self.txt_apellido = Entry(self.label_client, textvariable=self.apellidos_f, width=40)
        self.txt_apellido.bind('<Return>', self.sig_entry2)
        self.txt_apellido.place(x=160, y=70)

        lbl_direccion = Label(self.label_client, text=' DIRECCIÓN ',
                              font=('Copperplate Gothic Bold', 10), width=15, bg='#808080')
        lbl_direccion.place(x=10, y=100)
        self.direccion_f = StringVar()
        self.txt_direccion = Entry(self.label_client, textvariable=self.direccion_f, width=55)
        self.txt_direccion.place(x=160, y=100)

        self.add_btn = Button(self.label_client, image=self.imagenes['facturar'], text=' REGISTAR ',
                              command=self.guardar_cliente, compound=LEFT)
        self.add_btn.image = self.imagenes['facturar']
        self.add_btn.place(x=210, y=130)

    def sig_entry(self, event):
        if self.id_cliente.get() == '':
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: No. CÉDULA!!!")
            self.txt_codigo.focus()

        else:
            a = self.txt_codigo.get()
            if self.txt_codigo.get() == "":
                messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: No. CÉDULA!!!")
                self.txt_codigo.focus()

            elif a.isalpha():
                messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "NO SE ADMITEN LETRAS EN EL CAMPO DE "
                                                                              "BÚSQUEDA")
                self.id_cliente.set("")
                self.txt_codigo.focus()

            elif a.isspace():
                messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "NO SE PERMITEN ESPACIOS EN EL CAMPO DE "
                                                                              "BÚSQUEDA!!!")
                self.id_cliente.set("")
                self.txt_codigo.focus()

            else:
                if len(a) == 10:
                    self.txt_nombre.focus()

                else:
                    messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "No. DE CÉDULA NO VÁLIDO!!!\n"
                                                                                  "INGRESE NUEVAMENTE")
                    self.id_cliente.set("")
                    self.txt_codigo.focus()

    def sig_entry1(self, event):
        if self.txt_nombre.get() == '':
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: NOMBRES!!!")
            self.txt_nombre.focus()

        else:
            self.txt_apellido.focus()

    def sig_entry2(self, event):
        if self.txt_apellido.get() == '':
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: APELLIDOS!!!")
            self.txt_apellido.focus()

        else:
            self.txt_direccion.focus()

    def guardar_cliente(self):
        if self.txt_codigo.get() == "":
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: No. CÉDULA!!!")
            self.txt_codigo.focus()

        elif self.txt_nombre.get() == "":
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: NOMBRES!!!")
            self.txt_nombre.focus()

        elif self.txt_apellido.get() == "":
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: APELLIDOS!!!")
            self.txt_apellido.focus()

        elif self.txt_direccion.get() == "":
            messagebox.showwarning("SYST_CONTROL(IFAP®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: DIRECCIÓN!!!")
            self.txt_direccion.focus()

        else:
            # Guarda un cliente
            cliente = Cliente()
            cliente.id = self.txt_codigo.get()
            cliente.nombre = self.txt_apellido.get() + " " + self.txt_nombre.get()
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
        Principal_Window_A.Principal(root)
        self.root.withdraw()
        root.deiconify()

    def producto_btn(self):
        root = Toplevel()
        Producto_Window_A.Producto_w(root)
        self.root.withdraw()
        root.deiconify()

    def materia_prima_btn(self):
        root = Toplevel()
        Materia_Prima_Window_A.Materia_P(root)
        self.root.withdraw()
        root.deiconify()

    def proveedor_btn(self):
        root = Toplevel()
        Proveedor_Window_A.Proveedor_W(root)
        self.root.withdraw()
        root.deiconify()

    def materia_prima_c_btn(self):
        root = Toplevel()
        Materia_Prima_Window_A.Materia_P(root)
        self.root.withdraw()
        root.deiconify()

    def report_btn(self):
        root = Toplevel()
        Report_Window_A.Reports(root)
        self.root.withdraw()
        root.deiconify()

    def pass_btn(self):
        root = Toplevel()
        Password_Window_A.Password(root)
        self.root.withdraw()
        root.deiconify()

    def users_btn(self):
        root = Toplevel()
        Users_Window_A.Users(root)
        self.root.withdraw()
        root.deiconify()

    def ver_fct_btn(self):
        root = Toplevel()
        Re_Facturation.Ventana_Principal_1(root)
        self.root.withdraw()
        root.deiconify()

    def salir_principal(self):
        self.sa = messagebox.askyesno('CERRAR SESIÓN', 'CERRAR SYST_CONTROL(IFAP®)')
        if self.sa:
            raise SystemExit

    # =============================================================
    # FUNCIÓN CAJA DE INFORMACIÓN DEL SISTEMA(INFO)
    # =============================================================
    def caja_info_sist(self):
        self.men2 = messagebox.showinfo('SIST_CONTROL (IFAP®)',
                                        'SIST_CONTROL (IFAP®) v2.0\n'
                                        'El uso de este software queda sujeto a los términos y condiciones del '
                                        'contrato "J.C.F DESING®-CLIENTE".    \n'
                                        'El uso de este software queda sujeto a su contrato. No podrá utilizar '
                                        'este software para fines de distribución\n'
                                        'total o parcial.\n\n\n© 2021 J.C.F DESING®. Todos los derechos reservados')


def root():
    root = tk.ThemedTk()
    root.get_themes()
    root.set_theme("arc")
    Facturation(root)
    root.mainloop()


if __name__ == '__main__':
    root()

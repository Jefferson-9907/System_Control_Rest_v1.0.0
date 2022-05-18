import random
from time import strftime
from tkinter import *
from tkinter import messagebox

from ttkthemes import themed_tk as tk
from tkinter.ttk import Treeview, Combobox
from datetime import datetime

import Facturation_Window_A
from modelos import Factura, ProductoFacturar
from funciones_auxiliares import conexion_consulta

import login_form
import Principal_Window_C
import Facturation_Window_C
import Password_Window_C
import Users_Window_C


class Ventana_Principal_1:
    """
        Contiene todos los widgets necesario para la facturacion
    """

    def __init__(self, root):

        self.root = root
        self.root.title("SYST_CONTROL--›Facturación")
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.iconbitmap('recursos\\icon_rest.ico')
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

        self.txt = "SYSTEM CONTROL IFAP (VERIFICAR FACTURA)"
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
        self.menubarra.add_cascade(label='PARALELOS')
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
        # AÑADIENDO OPCIONES AL MENÚ ALUMNO
        # =============================================================
        self.menus.add_cascade(label='ALUMNOS', menu=self.Column2)
        self.Column2.add_command(label='Alumnos', command=self.student_btn)
        self.Column2.add_command(label='Matriculación', command=self.matricula_btn)
        self.Column3 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL MENÚ ASESORES
        # =============================================================
        self.menus.add_cascade(label='ASESORES', menu=self.Column3)
        self.Column3.add_command(label='Asesores')
        self.Column4 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ CURSOS
        # =============================================================
        self.menus.add_cascade(label='CURSOS', menu=self.Column4)
        self.Column4.add_command(label='Menú Cursos')
        self.Column4.add_command(label='Menú Paralelos')
        self.Column4.add_command(label='Implementos')
        self.Column5 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ FACTURACIÓN
        # =============================================================
        self.menus.add_cascade(label='FACTURACIÓN', menu=self.Column5)
        self.Column5.add_command(label='Facturación', command=self.facturation_btn)
        self.Column5.add_command(label='Reimpresión Factura')
        self.Column6 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ REPORTES
        # =============================================================
        self.menus.add_cascade(label='REPORTES', menu=self.Column6)
        self.Column6.add_command(label='Generar Reportes', command=self.report_btn)
        self.Column7 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ USUARIOS
        # =============================================================
        self.menus.add_cascade(label='USUARIOS', menu=self.Column7)
        self.Column7.add_command(label='Cambiar Usuario')
        self.Column7.add_command(label='Cambiar Contraseña')
        self.Column7.add_separator()
        self.Column7.add_command(label='Cerrar Sesión')
        self.Column7.add_separator()
        self.Column8 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ INFO
        # =============================================================
        self.menus.add_cascade(label='INFO', menu=self.Column8)
        self.Column8.add_command(label='Sobre SIST_CONTROL (IFAP®)')
        self.Column8.add_separator()
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

        self.factura = Factura()
        self.widget_facturacion()

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

    def widget_facturacion(self):
        """
             Ventana que asocia todos los controles e informacion
             acerca de la facturacion de un producto, no disponible cuando
             inicia, para acceder a ella presionar el boton nueva venta
        """
        self.label_facturacion = LabelFrame(self.root, width=1335, height=605, bg='#a27114')
        self.label_facturacion.place(x=15, y=85)

        self.lb_cod_factura = Label(self.label_facturacion, text='CÓD. FACTURA', bg='#a27114', fg="White",
                                    font=("Copperplate Gothic Bold", 12, "bold"))
        self.lb_cod_factura.place(x=420, y=10)

        self.codigo_factura = StringVar()
        self.txt_cod_factura = Entry(self.label_facturacion, textvariable=self.codigo_factura,
                                     fg='Red', width=14, font=('Copperplate Gothic Bold', 14), relief=RIDGE)
        self.txt_cod_factura.place(x=580, y=10)

        self.btnBuscar = Button(self.label_facturacion, image=self.imagenes['buscar'], text='BUSCAR', width=80,
                                command=self.obtener_factura, compound=RIGHT)
        self.btnBuscar.image = self.imagenes['buscar']
        self.btnBuscar.place(x=790, y=5)

        self.label_facturacion_1 = LabelFrame(self.root, text='Datos para factura', width=1310, height=100,
                                              bg='#a27114')
        self.label_facturacion_1.place(x=25, y=130)

        self.search_field = StringVar()
        self.l_ced_al = Label(self.label_facturacion_1, text='No. CÉDULA', font=('Copperplate Gothic Bold', 10),
                              bg='#808080')
        self.l_ced_al.place(x=10, y=10)
        self.cliente = Entry(self.label_facturacion_1, textvariable=self.search_field, width=19, state='readonly')
        self.cliente.place(x=110, y=10)

        self.l_name = Label(self.label_facturacion_1, text='NOMBRES', font=('Copperplate Gothic Bold', 10), width=10,
                            bg='#808080')
        self.l_name.place(x=10, y=40)
        self.nombres_f = StringVar()
        self.name_e = Entry(self.label_facturacion_1, width=45, textvariable=self.nombres_f, state='readonly')
        self.name_e.place(x=110, y=40)

        self.lb_direccion = Label(self.label_facturacion_1, text='DIRECCIÓN', font=('Copperplate Gothic Bold', 10),
                                  bg='#808080', width=10)
        self.lb_direccion.place(x=390, y=40)
        self.direcccion_f = StringVar()
        self.dir_e_al = Entry(self.label_facturacion_1, width=40, textvariable=self.direcccion_f, state='readonly')
        self.dir_e_al.place(x=490, y=40)

        self.lb_fecha = Label(self.label_facturacion_1, text='FECHA', font=('Copperplate Gothic Bold', 10),
                              bg='#808080', width=10)
        self.lb_fecha.place(x=745, y=40)
        self.fecha_f = StringVar()
        self.fecha_e_f = Entry(self.label_facturacion_1, width=20, textvariable=self.fecha_f, state='readonly')
        self.fecha_e_f.place(x=845, y=40)

        self.lb_hora = Label(self.label_facturacion_1, text='HORA', font=('Copperplate Gothic Bold', 10),
                             bg='#808080', width=10)
        self.lb_hora.place(x=980, y=40)
        self.hora_f = StringVar()
        self.hora_e_f = Entry(self.label_facturacion_1, width=20, textvariable=self.hora_f, state='readonly')
        self.hora_e_f.place(x=1080, y=40)

        self.lb_detalle = Label(self.label_facturacion, text='-------DETALLE FACTURA-------', bg='#a27114', fg="White",
                                font=("Copperplate Gothic Bold", 16, "bold"))
        self.lb_detalle.place(x=500, y=160)

        self.detalle_factura = Treeview(self.label_facturacion, columns=('#0', '#1', '#2',), height=10)
        self.detalle_factura.place(x=15, y=200)
        self.detalle_factura.column('#0', width=975)
        self.detalle_factura.column('#1', width=100)
        self.detalle_factura.column('#2', width=100)
        self.detalle_factura.column('#3', width=100)

        self.detalle_factura.heading('#0', text='Implemento')
        self.detalle_factura.heading('#1', text='Cant.')
        self.detalle_factura.heading('#2', text='Precio')
        self.detalle_factura.heading('#3', text='Subtotal')

        self.total = StringVar()
        self.lb_total = Label(self.label_facturacion, text='TOTAL    $', font=("Copperplate Gothic Bold", 11, "bold"),
                              bg='#a27114', fg="White")
        self.lb_total.place(x=1150, y=475)
        self.tx_total = Entry(self.label_facturacion, state='readonly', textvariable=self.total, width=10)
        self.tx_total.place(x=1255, y=475)

        self.pago = StringVar()
        self.lb_pago = Label(self.label_facturacion, text='PAGO      $', font=("Copperplate Gothic Bold", 11, "bold"),
                             bg='#a27114', fg="White")
        self.lb_pago.place(x=1150, y=505)

        self.txt_pago = Entry(self.label_facturacion, state='readonly', textvariable=self.pago, width=10)
        self.txt_pago.place(x=1255, y=505)

        self.cambio = StringVar()
        self.lb_cambio = Label(self.label_facturacion, text='CAMBIO $', font=("Copperplate Gothic Bold", 11, "bold"),
                               bg='#a27114', fg="White")
        self.lb_cambio.place(x=1150, y=535)
        self.tx_cambio = Entry(self.label_facturacion, state='readonly', textvariable=self.cambio, width=10)
        self.tx_cambio.place(x=1255, y=535)

        self.lb_moneda = Label(self.label_facturacion, text='Moneda', font=("Copperplate Gothic Bold", 11, "bold"),
                               bg='#a27114', fg="White")
        self.lb_moneda.place(x=850, y=475)
        self.tipo_moneda = Combobox(self.label_facturacion, values=['$-USD', '€-EUR '], width=10)
        self.tipo_moneda.place(x=950, y=475)

        """self.BtnFacturar = Button(self.label_facturacion, image=self.imagenes['print'], text='RE-IMPRIMIR', width=80,
                                  command=self.guardar_factura, compound=TOP)
        self.BtnFacturar.image = self.imagenes['print']
        self.BtnFacturar.place(x=950, y=505)"""

    def obtener_factura(self):
        self.cod_f = self.codigo_factura.get()
        # Lista todos los cliente y lo muestra en el combobox de factura
        consulta = 'SELECT * FROM Factura WHERE id_factura=?'
        parametros = [self.cod_f]
        data = conexion_consulta(consulta, parametros)
        for values in data:
            data_list_c = str(values[1])
            data_list_f = str(values[2])
            data_list_h = str(values[3])
            data_list_t = str(values[4])
            data_list_p = str(values[5])

            self.search_field.set(data_list_c)
            self.fecha_f.set(data_list_f)
            self.hora_f.set(data_list_h)
            self.obtener_clientes()
            self.total.set(data_list_t)
            self.pago.set(data_list_p)
            self.calcular_cambio()
            self.obtener_det_fact()

    def obtener_clientes(self):
        self.n_c_cl = self.search_field.get()
        # Lista todos los cliente y lo muestra en el combobox de factura
        consulta = 'SELECT * FROM Cliente WHERE ID=?'
        parametros = [self.n_c_cl]
        data = conexion_consulta(consulta, parametros)
        for values in data:
            data_list_n = str(values[1])
            data_list_d = str(values[2])
            self.nombres_f.set(data_list_n)
            self.direcccion_f.set(data_list_d)

    def obtener_det_fact(self):
        consulta = 'SELECT producto.nombre, detallefact.cantidad, detallefact.precio_unit, detallefact.sub_total ' \
                   'FROM detallefact JOIN producto ON producto.id = detallefact.id_producto ' \
                   'WHERE id_factura=?'
        parametros = [self.cod_f]
        data = conexion_consulta(consulta, parametros)

        registros = self.detalle_factura.get_children()
        for items in registros:
            self.detalle_factura.delete(items)

        for element in data:
            self.detalle_factura.insert('', 0, text=element[0], values=(element[1],
                                                                        element[2],
                                                                        element[3],
                                                                        )
                                        )

    def calcular_cambio(self):
        # Calcula el cambio
        billete = float(self.txt_pago.get())
        cambio = billete - float(self.total.get())
        self.cambio.set(str(cambio))

    def agregar_producto_factura(self, ):
        """
             Funcion asociada para agregar un producto a la factura
        """
        producto_factura = ProductoFacturar()
        producto_factura.id_factura = self.codigo_factura.get()
        self.factura.lista_productos.append(producto_factura)

        consulta = 'SELECT producto.id, producto.nombre, detallefact.cantidad, detallefact.precio_unit, ' \
                   'detallefact.sub_total FROM detallefact JOIN producto ON producto.id = detallefact.id_producto ' \
                   'WHERE id_factura=?'
        parametros = [self.cod_f]
        data = conexion_consulta(consulta, parametros)

        registros = self.detalle_factura.get_children()
        for items in registros:
            self.detalle_factura.delete(items)

        for values in data:
            self.id_impl = StringVar()
            self.nom_impl = StringVar()
            self.pvp_impl = StringVar()
            self.can_impl = StringVar()
            self.subt_impl = StringVar()

            data_list_id = str(values[0])
            data_list_n = str(values[1])
            data_list_p = str(values[2])
            data_list_c = str(values[3])
            data_list_s = str(values[4])

            self.id_impl = self.id_impl.set(data_list_id)
            self.nom_impl = self.nom_impl.set(data_list_n)
            self.pvp_impl = self.pvp_impl.set(data_list_p)
            self.can_impl = self.can_impl.set(data_list_c)
            self.subt_impl = self.subt_impl.set(data_list_s)

            producto_factura.id = self.id_impl
            producto_factura.nombre = self.nom_impl
            producto_factura.precio_venta = self.pvp_impl
            producto_factura.cantidad = self.can_impl
            producto_factura.sub_total = self.subt_impl

            self.factura.lista_productos.append(producto_factura)

    def guardar_factura(self):
        pass
        """
            Guarda el registro de la factura
        """
        """if self.txt_pago != '':  # Si el pago no esta vacio
            factura = self.factura

            for productos_factura in self.factura.lista_productos:
                productos_factura.re_imprimir()

            factura.id_factura = self.codigo_factura.get()
            id_cliente = self.cliente.get()
            lista_cliente = id_cliente.split('_')
            factura.id_cliente = lista_cliente[0]
            fecha = datetime.now()
            factura.fecha_creacion = '{}-{}-{}'.format(fecha.day, fecha.month, fecha.year)
            factura.hora_creacion = '{}:{}'.format(fecha.hour, fecha.day)
            factura.pago = self.txt_pago.get()
            factura.cambio = self.cambio.get()
            self.agregar_producto_factura()
            recibo = ReciboFactura()  # Instancia del recibo factura
            recibo.detalles_factura(factura)  # se pasa el objeto para ser llenado el recibo
            recibo.save()
        else:
            pass"""

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

    def student_btn(self):
        root = Toplevel()
        Student_Window_A.Student(root)
        self.root.withdraw()
        root.deiconify()

    def matricula_btn(self):
        root = Toplevel()
        Matricula_Window_A.Matricula(root)
        self.root.withdraw()
        root.deiconify()

    def assesor_btn(self):
        root = Toplevel()
        Assesor_Window_A.Assesor(root)
        self.root.withdraw()
        root.deiconify()

    def courses_btn(self):
        root = Toplevel()
        Course_Window_A.Course(root)
        self.root.withdraw()
        root.deiconify()

    def paralelos_btn(self):
        root = Toplevel()
        Paralelo_Window_A.Paralelo(root)
        self.root.withdraw()
        root.deiconify()

    def facturation_btn(self):
        root = Toplevel()
        Facturation_Window_A.Ventana_Principal(root)
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
    Ventana_Principal_1(root)
    root.mainloop()


if __name__ == '__main__':
    root()

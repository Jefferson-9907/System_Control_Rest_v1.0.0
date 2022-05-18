# Import Modules
import sqlite3
from _datetime import datetime
from time import strftime
from tkinter import *
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import random

from modelos import Materia_prima

import Principal_Window_A
import login_form
import Producto_Window_A
import Proveedor_Window_A
import Materia_Prima_C_Window_A
import Password_Window_A
import Users_Window_A


class Materia_P:
    """
        Permite a los administradores gestionar a los estudiantes; añadir, actualizar, eliminar, obtener los datos,
        aquí, el administrador puede ver todos los detalles de estudiantes y tener varias opciones para realizar,
        pueden buscarlos por nombre, esto se hizo mediante el uso de la función de comodín de MySQL después de
        agarrar todos los datos y luego realizar la ordenación de burbuja en eso y más tarde enviado al método de
        búsqueda binaria si los datos existen entonces todos los datos.
    """
    list_of_tree = []
    get_id = []

    def __init__(self, root):
        self.root = root
        self.root.title("SYST_CONTROL(REST®)--›(MATERIA PRIMA)")
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.iconbitmap('recursos\\icon_rest.ico')
        self.root.configure(bg='#a27114')

        self.imagenes = {
            'nuevo': PhotoImage(file='recursos\\icon_aceptar.png'),
            'matricular': PhotoImage(file='recursos\\icon_add.png'),
            'editar': PhotoImage(file='recursos\\icon_update.png'),
            'eliminar': PhotoImage(file='recursos\\icon_del.png'),
            'limpiar': PhotoImage(file='recursos\\icon_clean.png'),
            'buscar': PhotoImage(file='recursos\\icon_buscar.png'),
            'todo': PhotoImage(file='recursos\\icon_ver_todo.png'),
            'actualizar': PhotoImage(file='recursos\\icon_upd.png')
        }

        # =============================================================
        # BANNER PANTALLA ESTUDIANTES
        # =============================================================

        self.txt = "SYSTEM CONTROL REST® (MATERIA PRIMA)"
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
        self.Column2.add_command(label='Materia Prima')
        self.Column2.add_command(label='Producto', command=self.platos_btn)
        self.Column3 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: COMPRA AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='COMPRA', menu=self.Column3)
        self.Column3.add_command(label='Proveedor', command=self.proveedor_btn)
        self.Column3.add_command(label='Materia Prima', command=self.materia_prima_c_btn)
        self.Column4 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: VENTA AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='VENTA', menu=self.Column4)
        self.Column4.add_command(label='Tiket')
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

        self.m_prima = Materia_prima()

        # Manage Frame
        Manage_Frame = Frame(self.root, relief=RIDGE, bd=4, bg='#a27114')
        Manage_Frame.place(x=15, y=85, width=385, height=605)

        self.e_id_materia_p_1 = StringVar()
        self.e_descripcion_1 = StringVar()
        self.e_l_u_medida_1 = StringVar()
        self.e_cantidad_1 = StringVar()
        self.e_observacion_1 = StringVar()
        self.search_entry = StringVar()

        m_title = Label(Manage_Frame, text="-ADM. MATERIA PRIMA-", font=("Copperplate Gothic Bold", 16, "bold"),
                        bg='#a27114', fg="White")
        m_title.grid(row=0, columnspan=2, padx=10, pady=50)

        self.l_id_materia_p = Label(Manage_Frame, text='CÓD.', width='15', font=('Copperplate Gothic Bold', 10),
                                    bg='#808080')
        self.l_id_materia_p.grid(column=0, row=1, padx=0, pady=5)
        self.e_id_materia_p = Entry(Manage_Frame, textvariable=self.e_id_materia_p_1, width=10, state="disabled")
        self.e_id_materia_p.grid(column=1, row=1, padx=0, pady=5, sticky="W")

        self.l_descripcion = Label(Manage_Frame, text='DESCRICIÓN', width='15', font=('Copperplate Gothic Bold', 10),
                                   bg='#808080')
        self.l_descripcion.grid(column=0, row=2, padx=1, pady=5)
        self.e_descripcion = Entry(Manage_Frame, textvariable=self.e_descripcion_1, width=33)
        self.e_descripcion.bind('<Return>', self.sig_entry)
        self.e_descripcion.grid(column=1, row=2, padx=1, pady=5, sticky="W")
        self.e_descripcion.focus()

        self.l_u_medida = Label(Manage_Frame, text='U. MEDIDA', width='15', font=('Copperplate Gothic Bold', 10),
                                bg='#808080')
        self.l_u_medida.grid(column=0, row=3, padx=0, pady=5)
        self.e_l_u_medida = Entry(Manage_Frame, textvariable=self.e_l_u_medida_1, width=10, state="disabled")
        self.e_l_u_medida_1.set('0')
        self.e_l_u_medida.grid(column=1, row=3, padx=0, pady=5, sticky="W")

        self.l_cantidad = Label(Manage_Frame, text='CANTIDAD', width='15', font=('Copperplate Gothic Bold', 10),
                                bg='#808080')
        self.l_cantidad.grid(column=0, row=4, padx=0, pady=5)
        self.e_cantidad = Entry(Manage_Frame, textvariable=self.e_cantidad_1, width=10, state="disabled")
        self.e_cantidad_1.set('0')
        self.e_cantidad.grid(column=1, row=4, padx=0, pady=5, sticky="W")

        self.l_observacion = Label(Manage_Frame, text='OBSERV.', width='15', font=('Copperplate Gothic Bold', 10),
                                   bg='#808080')
        self.l_observacion.grid(column=0, row=5, padx=1, pady=5)
        self.e_observacion = Entry(Manage_Frame, textvariable=self.e_observacion_1, width=33)
        self.e_observacion_1.set("S/O")
        self.e_observacion.grid(column=1, row=5, padx=1, pady=5, sticky="W")

        # Button Frame
        self.btn_frame = Frame(Manage_Frame, bg='#a27114')
        self.btn_frame.place(x=10, y=500, width=360)

        self.add_btn = Button(self.btn_frame, image=self.imagenes['nuevo'], text='REGISTAR', command=self.add_materia_p,
                              compound=TOP)
        self.add_btn.image = self.imagenes['nuevo']
        self.add_btn.grid(row=0, column=0, padx=3, pady=10)

        self.up_btn = Button(self.btn_frame, image=self.imagenes['editar'], text='MODIFICAR', command=self.update,
                             compound=TOP)
        self.up_btn.image = self.imagenes['editar']
        self.up_btn.grid(row=0, column=2, padx=3, pady=10)
        self.up_btn["state"] = "disabled"

        self.del_btn = Button(self.btn_frame, image=self.imagenes['eliminar'], text='ELIMINAR', command=self.delete,
                              compound=TOP)
        self.del_btn.image = self.imagenes['eliminar']
        self.del_btn.grid(row=0, column=3, padx=3, pady=10)
        self.del_btn["state"] = "disabled"

        self.clean_btn = Button(self.btn_frame, image=self.imagenes['limpiar'], text='LIMPIAR',
                                command=self.clear_field, compound=TOP)
        self.clean_btn.image = self.imagenes['limpiar']
        self.clean_btn.grid(row=0, column=4, padx=3, pady=10)

        # Detail Frame
        self.Detail_Frame = Frame(self.root, bd=4, relief=RIDGE, bg='#a27114')
        self.Detail_Frame.place(x=405, y=85, width=940, height=605)

        self.lbl_search = Label(self.Detail_Frame, text="BUSCAR", bg='#a27114', fg="White",
                                font=("Copperplate Gothic Bold", 12, "bold"))
        self.lbl_search.grid(row=0, column=0, pady=10, padx=2, sticky="w")

        self.txt_search = Entry(self.Detail_Frame, width=15, textvariable=self.search_entry,
                                font=("Arial", 10, "bold"), bd=5, relief=GROOVE)
        self.txt_search.grid(row=0, column=1, pady=10, padx=5, ipady=4, sticky="w")

        self.search_btn = Button(self.Detail_Frame, image=self.imagenes['buscar'], text='BUSCAR', width=80,
                                 command=self.search_data, compound="right")
        self.search_btn.image = self.imagenes['buscar']
        self.search_btn.grid(row=0, column=2, padx=10, pady=10)

        self.show_all_btn = Button(self.Detail_Frame, image=self.imagenes['todo'], text='VER TODO', width=80,
                                   command=self.show_data, compound="right")
        self.show_all_btn.image = self.imagenes['todo']
        self.show_all_btn.grid(row=0, column=3, padx=10, pady=10)

        self.act_btn = Button(self.Detail_Frame, image=self.imagenes['actualizar'], text='ACTUALIZAR', width=100,
                              command=self.principal_btn, compound="right")
        self.act_btn.image = self.imagenes['actualizar']
        self.act_btn.grid(row=0, column=4, padx=10, pady=10)

        # Table Frame

        Table_Frame = Frame(self.Detail_Frame)
        Table_Frame.place(x=5, y=60, width=920, height=535)

        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.Table = ttk.Treeview(Table_Frame, columns=("co", "des", "can", "ob"),
                                  xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Table.xview)
        scroll_y.config(command=self.Table.yview)

        self.Table.heading("co", text="CÓD. ")
        self.Table.heading("des", text="DESCRIPCIÓN")
        self.Table.heading("can", text="CANTIDAD")
        self.Table.heading("ob", text="OBSERVACIÓN")

        self.Table['show'] = "headings"
        self.Table.column("co", width=10)
        self.Table.column("des", width=200)
        self.Table.column("can", width=50)
        self.Table.column("ob", width=250)

        self.Table.pack(fill=BOTH, expand=1)
        self.Table.bind('<ButtonRelease 1>', self.get_fields)

        self.show_data()

    def sig_entry(self, event):
        a = self.e_descripcion_1.get()
        if self.e_descripcion.get() == '':
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "INGRESE EL CAMPO: DESCRIPCIÓN!!!")
            self.e_descripcion.focus()

        elif a.isnumeric():
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "NO SE ADMITEN NÚMEROS EN EL CAMPO: "
                                                                          "DESCRIPCIÓN")
            self.e_descripcion_1.set("")
            self.e_descripcion.focus()

        elif a.isspace():
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "NO SE PERMITEN ESPACIOS EN EL CAMPO: "
                                                                          "DESCRIPCIÓN")
            self.e_descripcion_1.set("")
            self.e_descripcion.focus()

        else:
            self.e_observacion.focus()

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

    def add_materia_p(self):
        if self.e_descripcion_1.get() == "" or self.e_observacion_1.get() == "":
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "TODOS LOS CAMPOS SON OBLIGATORIOS!!!")

        else:
            self.click_submit()

    def click_submit(self):
        self.e_cantidad_1 = "0"
        """
            Inicializar al hacer clic en el botón enviar, que tomará los datos del cuadro de entrada
            e inserte esos datos en la tabla de estudiantes después de la validación exitosa de esos datos
        """
        materia_prima = self.m_prima
        materia_prima.descripcion = self.e_descripcion_1.get()
        materia_prima.cantidad = self.e_cantidad_1
        materia_prima.observacion = self.e_observacion_1.get()
        materia_prima.guardar()
        self.show_data()
        self.clear_field()

    def clear_field(self):
        self.e_id_materia_p_1.set('')
        self.e_descripcion_1.set('')
        self.e_cantidad_1.set('0')
        self.e_observacion_1.set('')
        self.add_btn["state"] = "normal"
        self.up_btn["state"] = "disabled"
        self.del_btn["state"] = "disabled"

    def get_fields(self, row):
        self.cursor_row = self.Table.focus()
        self.content = self.Table.item(self.cursor_row)
        row = self.content['values']

        self.e_id_materia_p_1.set(str(row[0]))
        self.e_descripcion_1.set(row[1])
        self.e_cantidad_1.set(str(row[2]))
        self.e_observacion_1.set(row[3])
        self.add_btn["state"] = "disabled"
        self.up_btn["state"] = "normal"
        self.del_btn["state"] = "normal"

    def validation(self):
        if self.e_descripcion_1.get() == '' or self.e_cantidad_1.get() == '' or self.e_observacion_1.get() == '':
            messagebox.showerror("SYST_CONTROL(REST®)-->(ERROR)", "TODOS LOS CAMPOS SON OBLIGATORIOS!!!")

        else:
            self.update()

    def update(self):
        materia_prima = self.m_prima
        materia_prima.descripcion = self.e_descripcion_1.get()
        materia_prima.cantidad = self.e_cantidad_1.get()
        materia_prima.observacion = self.e_observacion_1.get()
        materia_prima.id = self.e_id_materia_p_1.get()
        materia_prima.actualizar()
        self.show_data()
        self.clear_field()

    def delete(self):
        materia_prima = self.m_prima
        materia_prima.descripcion = self.e_descripcion_1.get()
        materia_prima.eliminar()
        self.show_data()
        self.clear_field()

    # =======================================================================
    # ========================Searching Started==============================
    # =======================================================================
    @classmethod
    def binary_search(cls, _list, target):
        """this is class method searching for user input into the table"""
        start = 0
        end = len(_list) - 1

        while start <= end:
            middle = (start + end) // 2
            midpoint = _list[middle]
            if midpoint > target:
                end = middle - 1
            elif midpoint < target:
                start = middle + 1
            else:
                return midpoint

    @classmethod
    def bubble_sort(self, _list):
        """this class methods sort the string value of user input such as name, email"""
        for j in range(len(_list) - 1):
            for i in range(len(_list) - 1):
                if _list[i].upper() > _list[i + 1].upper():
                    _list[i], _list[i + 1] = _list[i + 1], _list[i]
        return _list

    def search_data(self):
        a = self.search_entry.get()
        if self.search_entry.get() != '':
            if a.isnumeric():
                messagebox.showerror("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "NO SE ADMITEN NÚMEROS EN EL CAMPO DE "
                                                                            "BÚSQUEDA DE ESTUDIANTE")
                self.search_entry.set("")
            elif a.isspace():
                messagebox.showerror("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "NO SE ADMITEN ESPACIOS EN EL CAMPO DE "
                                                                            "BÚSQUEDA DE ESTUDIANTE")
                self.search_entry.set("")
            else:
                if a.isalpha():
                    try:
                        search_list = []
                        for child in self.Table.get_children():
                            val = self.Table.item(child)["values"][1]
                            search_list.append(val)

                        sorted_list = self.bubble_sort(search_list)
                        self.output = self.binary_search(sorted_list, self.search_entry.get())

                        if self.output:
                            messagebox.showinfo("SYST_CONTROL(REST®)-->(ENCONTRADO)",
                                                f"MATERIA PRIMA: '{self.output}' HA SIDO ENCONTRADA")

                            with sqlite3.connect('ddbb_sys_rest.db') as conexion:
                                try:  # Captura la excepcion en caso de que algo falle
                                    cursor = conexion.cursor()
                                    data = cursor.execute(
                                        "SELECT * FROM INV_MATERIA_P WHERE descripcion LIKE '" + str(
                                            self.search_entry) + "%'")

                                    self.Table.delete(*self.Table.get_children())

                                    for values in data:
                                        data_list = [values[0], values[1], values[2], values[3]]
                                        self.Table.insert('', END, values=data_list)

                                except Exception as e:
                                    print(e)
                                    conexion.close()
                                    return False

                        else:
                            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)",
                                                   "MATERIA PRIMA NO ENCONTRADO,\nSE MOSTRARÁN RESULTADOS RELACIONADOS.")

                            with sqlite3.connect('ddbb_sys_rest.db') as conexion:
                                try:  # Captura la excepcion en caso de que algo falle
                                    cursor = conexion.cursor()
                                    data = cursor.execute(
                                        "SELECT * FROM INV_MATERIA_P WHERE descripcion LIKE '%" + str(
                                            self.search_entry) + "%'")

                                    self.Table.delete(*self.Table.get_children())

                                    for values in data:
                                        data_list = [values[0], values[1], values[2], values[3]]
                                        self.Table.insert('', END, values=data_list)

                                except Exception as e:
                                    print(e)
                                    conexion.close()
                                    return False

                    except BaseException as msg:
                        messagebox.showerror("SYST_CONTROL(REST®)-->(ERROR)",
                                             f"NO FUÉ POSIBLE CONECTARSE CON EL SERVIDOR,\n"
                                             f"REVISE LA CONEXIÓN: {msg}")
                else:
                    self.show_data()
        else:
            messagebox.showwarning("SYST_CONTROL(REST®)-->(ADVERTENCIA)", "EL CAMPO DE BÚSQUEDA SE ENCUENTRA VACÍO\n"
                                                                          "INGRESE EL NOMBRE DE LA MATERIA PRIMA.")

    def show_data(self):
        with sqlite3.connect('ddbb_sys_rest.db') as conexion:
            try:  # Captura la excepcion en caso de que algo falle
                cursor = conexion.cursor()
                data = cursor.execute('SELECT id_materia_prima, descripcion, stock, observacion FROM INV_MATERIA_P')

                self.Table.delete(*self.Table.get_children())
                for values in data:
                    data_list = [values[0], values[1], values[2], values[3]]
                    self.Table.insert('', END, values=data_list)

            except Exception as e:
                print(e)
                conexion.close()
                return False

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

    def platos_btn(self):
        root = Toplevel()
        Producto_Window_A.Producto_w(root)
        self.root.withdraw()
        root.deiconify()

    def proveedor_btn(self):
        root = Toplevel()
        Proveedor_Window_A.Proveedor_W(root)
        self.root.withdraw()
        root.deiconify()

    def materia_prima_c_btn(self):
        root = Toplevel()
        Materia_Prima_C_Window_A.Materia_P_C(root)
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
        self.sa = messagebox.askyesno('SYST_CONTROL(REST®)-->(CERRAR SESIÓN)', 'CERRAR SYST_CONTROL(REST®)')
        if self.sa:
            raise SystemExit

    # =============================================================
    # FUNCIÓN CAJA DE INFORMACIÓN DEL SISTEMA(INFO)
    # =============================================================
    def caja_info_sist(self):
        self.men2 = messagebox.showinfo('SYST_CONTROL(REST®)-->(INFORMACIÓN)',
                                        'SIST_CONTROL (REST®) v1.0\n'
                                        'El uso de este software queda sujeto a los términos y condiciones del '
                                        'contrato "J.C.F DESING®-CLIENTE".    \n'
                                        'El uso de este software queda sujeto a su contrato. No podrá utilizar '
                                        'este software para fines de distribución\n'
                                        'total o parcial.\n\n\n© 2022 J.C.F DESING®. Todos los derechos reservados')


def root():
    root = ThemedTk()
    root.get_themes()
    root.set_theme("arc")
    Materia_P(root)
    root.mainloop()


if __name__ == '__main__':
    root()

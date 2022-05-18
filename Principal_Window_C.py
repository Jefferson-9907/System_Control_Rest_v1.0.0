# Import Modules
import random
from datetime import datetime
from time import strftime
from tkinter import *
from ttkthemes import themed_tk as tk
from tkinter import messagebox

import login_form
import Facturation_Window_C
import Password_Window_C
import Re_Facturation
import sqlite3

from funciones_auxiliares import conexion_consulta
from modelos import Apertura


class Principal_C:

    def __init__(self, root):
        self.root = root
        self.root.title("SYST_CONTROL(REST®)--›(Principal)")
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.iconbitmap('recursos\\icon_rest.ico')

        self.imagenes = {
            'nuevo': PhotoImage(file='recursos\\icon_add.png'),
            'fondo': PhotoImage(file='recursos\\FONDO_PRINCIPAL.png'),
        }

        # =============================================================
        # FONDO PANTALLA PRINCIPAL
        # =============================================================
        self.fondo = Label(self.root, image=self.imagenes['fondo'], bg="#003366", fg='White',
                           font=("Cooper Black", 12), compound="left")
        self.fondo.image = self.imagenes['fondo']
        self.fondo.place(x=0, y=0)

        self.txt = "SYSTEM CONTROL REST® (INICIO)"
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
        # CREACIÓN DEL DE MENÚ FACTURACIÓN
        # =============================================================
        self.menus.add_cascade(label='VENTA', menu=self.Column1)
        self.Column1.add_command(label='Ticket', command=self.factura_btn)
        self.Column1.add_command(label='Verificar Factura', command=self.ver_fct_btn)
        self.Column2 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ AYUDA
        # =============================================================
        self.menus.add_cascade(label='USUARIOS', menu=self.Column2)
        self.Column2.add_command(label='Cambiar Usuario', command=self.logout)
        self.Column2.add_command(label='Cambiar Contraseña', command=self.pass_btn)
        self.Column2.add_separator()
        self.Column2.add_command(label='Cerrar Sesión', command=self.salir_principal)
        self.Column2.add_separator()
        self.Column3 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # CREACIÓN DEL DE MENÚ INFO
        # =============================================================
        self.menus.add_cascade(label='INFO', menu=self.Column3)
        self.Column3.add_command(label='Sobre SIST_CONTROL (REST®)', command=self.caja_info_sist)
        self.Column3.add_separator()
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

        self.fecha = datetime.now()
        self.fecha_creacion = '{}/{}/{}'.format(self.fecha.year, self.fecha.month, self.fecha.day)

        self.apertura_caja()

    def apertura_caja(self):
        with sqlite3.connect('ddbb_sys_rest.db') as conexion:
            try:  # Captura la excepcion en caso de que algo falle
                cursor = conexion.cursor()
                data = cursor.execute(f'SELECT EXISTS(SELECT * FROM INV_APERTURA_CAJA WHERE '
                                      f'fecha={self.fecha_creacion} LIMIT 1);')
                data1 = data.fetchone()
                if not data1:
                    print("EXISTE REGISTRO DE APARTURA DE CAJA")

                else:
                    print("NO EXISTE REGISTRO DE APARTURA DE CAJA")
                    self.ap_caja = Toplevel()
                    self.ap_caja.title("SYST_CONTROL(REST®)--›(Apertura Caja)")
                    self.ap_caja.geometry('450x100')
                    self.ap_caja.iconbitmap('recursos\\icon_rest.ico')
                    self.ap_caja.wait_visibility()
                    self.ap_caja.grab_set()
                    self.ap_caja.transient(master=self.root)

                    self.ape_caja = Apertura()

                    # Manage Frame
                    self.Manage_Frame_ac = Frame(self.ap_caja, relief=RIDGE, bd=4, bg='#a27114')
                    self.Manage_Frame_ac.place(x=0, y=0, width=450, height=100)

                    # Widgets para añadir un cliente
                    self.lbnumced = Label(self.Manage_Frame_ac, text='APERTURA $:',
                                          font=("Copperplate Gothic Bold", 20, "bold"),
                                          bg='#a27114', fg="White")
                    self.lbnumced.place(x=10, y=10)
                    self.txt_aper_caja_1 = DoubleVar()
                    self.txt_ap_caja = Entry(self.Manage_Frame_ac, textvariable=self.txt_aper_caja_1, width=7)
                    self.txt_ap_caja.focus()
                    self.txt_ap_caja.place(x=240, y=20)

                    self.btn_guardar = Button(self.Manage_Frame_ac, image=self.imagenes['nuevo'], text='GUARDAR',
                                              command=self.guardar_aperura, width=80, compound="right")
                    self.btn_guardar.image = self.imagenes['nuevo']
                    self.btn_guardar.place(x=175, y=50)

            except Exception as e:

                print(e)
                conexion.close()

    def guardar_aperura(self):
        self.id = IntVar()

        try:
            consulta = 'SELECT (id_apertura_caja+1) FROM INV_APERTURA_CAJA ORDER BY id_apertura_caja DESC LIMIT 1'
            codigo = conexion_consulta(consulta, parametros=())
            for values in codigo:
                data_list_id = values[0]
                self.id.set(data_list_id)

        except BaseException as msg:
            print(msg)

        self.ape_caja.id = self.id.get()
        self.ape_caja.cantidad = self.txt_aper_caja_1.get()
        self.fecha = datetime.now()
        self.ap_caja.fecha_creacion = self.fecha.replace()
        self.ape_caja.g_apertura()

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

    def logout(self):
        root = Toplevel()
        login_form.Login(root)
        self.root.withdraw()
        root.deiconify()

    def factura_btn(self):
        root = Toplevel()
        Facturation_Window_C.Facturation(root)
        self.root.withdraw()
        root.deiconify()

    def ver_fct_btn(self):
        root = Toplevel()
        Re_Facturation.Ventana_Principal_1(root)
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
    Principal_C(root)
    root.mainloop()


if __name__ == '__main__':
    root()

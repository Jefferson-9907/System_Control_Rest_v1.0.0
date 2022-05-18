# Import Modules
from _datetime import datetime
from time import strftime
from tkinter import *
from ttkthemes import themed_tk as tk
import random
from tkinter import messagebox

import login_form
import Materia_Prima_C_Window_A
import Producto_Window_A
import Materia_Prima_Window_A
import Proveedor_Window_A
import Password_Window_A
import Users_Window_A
import Report_a_us


class Principal:
    def __init__(self, root):
        self.root = root
        self.root.title("SYST_CONTROL(REST®)--›(Principal)")
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.iconbitmap('recursos\\icon_rest.ico')
        self.root.configure(bg='#a27114')

        imagenes = {
            'fondo': PhotoImage(file='recursos\\FONDO_PRINCIPAL.png'),
        }

        self.imagenes = {
            'nuevo': PhotoImage(file='recursos\\icon_aceptar.png')
        }

        # =============================================================
        # FONDO PANTALLA PRINCIPAL
        # =============================================================
        self.fondo = Label(self.root, image=imagenes['fondo'], bg="#003366", fg='White',
                           font=("Cooper Black", 12), compound="left")
        self.fondo.image = imagenes['fondo']
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
        # CREACIÓN DEL MENÚ
        # =============================================================
        self.menubarra.add_cascade(label='RESTAURANT')
        self.root.config(menu=self.menubarra)
        self.menus = Menu(self.root)
        self.Column1 = Menu(self.menus, tearoff=0)

        # =============================================================
        # AÑADIENDO OPCIÓN: INVENTARIO AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='INVENTARIO', menu=self.Column1)
        self.Column1.add_command(label='Materia Prima', command=self.materia_prima_btn)
        self.Column1.add_command(label='Producto', command=self.producto_btn)
        self.Column2 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: COMPRA AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='COMPRA', menu=self.Column2)
        self.Column2.add_command(label='Proveedor', command=self.proveedor_btn)
        self.Column2.add_command(label='Materia Prima', command=self.materia_prima_c_btn)
        self.Column3 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: VENTA AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='VENTA', menu=self.Column3)
        self.Column3.add_command(label='Tiket')
        self.Column3.add_command(label='Verificar Tíket')
        self.Column4 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: CAJA AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='CAJA', menu=self.Column4)
        self.Column4.add_command(label='Apertura')
        self.Column5 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: CUENTAS AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='CUENTAS', menu=self.Column5)
        self.Column5.add_command(label='Por Pagar')
        self.Column5.add_command(label='Por Cobrar')
        self.Column6 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: REPORTES AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='REPORTES', menu=self.Column6)
        self.Column6.add_command(label='Generar Reporte Usuarios', command=self.report_us)
        self.Column6.add_command(label='Generar Reporte Diario', command=self.report_us)
        self.Column7 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: USUARIOS AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='USUARIOS', menu=self.Column7)
        self.Column7.add_command(label='Cambiar Usuario', command=self.logout)
        self.Column7.add_command(label='Cambiar Contraseña', command=self.pass_btn)
        self.Column7.add_command(label='Usuarios', command=self.users_btn)
        self.Column7.add_separator()
        self.Column7.add_command(label='Cerrar Sesión', command=self.salir_principal)
        self.Column7.add_separator()
        self.Column8 = Menu(self.menus, tearoff=0)
        self.root.config(menu=self.menus)

        # =============================================================
        # AÑADIENDO OPCIÓN: INFO AL MENÚ
        # =============================================================
        self.menus.add_cascade(label='INFO', menu=self.Column8)
        self.Column8.add_command(label='Sobre SIST_CONTROL (REST®)', command=self.caja_info_sist)
        self.Column8.add_separator()
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

    def tic(self):
        self.clock["text"] = strftime("%H:%M:%S %p")

    def tac(self):
        self.tic()
        self.clock.after(1000, self.tac)

    def slider(self):
        """
            creates slides for heading by taking the text,
            and that text are called after every 100 ms
        """
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

    def report_us(self):
        Report_a_us.generarReporte_us()

    def report_dv(self):
        pass

    def logout(self):
        root = Toplevel()
        login_form.Login(root)
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
        self.sa = messagebox.askyesno('SIST_CONTROL (REST®) CERRAR SESIÓN', 'CERRAR SYST_CONTROL(REST®)')
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
    root = tk.ThemedTk()
    root.get_themes()
    root.set_theme("arc")
    Principal(root)
    root.mainloop()


if __name__ == '__main__':
    root()

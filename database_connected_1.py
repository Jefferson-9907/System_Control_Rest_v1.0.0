from tkinter import *
from PIL import ImageTk
from ttkthemes import themed_tk as tk
import random
import connection
from tkinter import messagebox
import login_form
import database_connected


class DatabaseConnected:
    """
        Clase a utilizar para luego de crear base de datos, creación de usuario administrador del sistema
    """
    email = []

    def __init__(self, root):
        """
            Toma la ventana para mostrar todos los atributos y la función de esta clase
        """
        self.root = root
        self.root.geometry("530x375")
        self.root.title("SYST_CONTROL(REST®)-(USUARIO ADMINISTRADOR)")
        self.root.iconbitmap('recursos\\icon_rest.ico')
        self.root.resizable(False, False)

        imagenes = {
            'new': PhotoImage(file='recursos\\icon_aceptar.png'),
            'login': PhotoImage(file='recursos\\icon_login.png'),
            'exit': PhotoImage(file='recursos\\icon_del.png'),
        }

        self.Manage_Frame_admin = Frame(self.root, bd=4, bg='#a27114')
        self.Manage_Frame_admin.place(x=0, y=0, width=530, height=375)

        self.login_frame = ImageTk.PhotoImage(file='recursos\\admin_setup_frame.png')
        self.image_panel = Label(self.Manage_Frame_admin, image=self.login_frame, bg='#a27114')
        self.image_panel.place(x=20, y=70)

        self.txt = "USUARIO ADMINISTRADOR"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("Cooper Black", 35), bg="#000000",
                             fg='black',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=0, y=0, width=530)
        self.slider()
        self.heading_color()

        self.db_connection = connection.DatabaseConnection()

        # ========================================================================
        # ==============================EMAIL=====================================
        # ========================================================================

        self.email_label = Label(self.Manage_Frame_admin, text="Email ", bg="#a27114", fg="Black",
                                 font=("yu gothic ui", 13, "bold"))
        self.email_label.place(x=75, y=65)

        self.email_entry = Entry(self.Manage_Frame_admin, highlightthickness=0, relief=FLAT, bg="#D3D3D3", fg="#4f4e4d",
                                 font=("yu gothic ui semibold", 12))
        self.email_entry.place(x=75, y=98, width=380)  # trebuchet ms

        # ========================================================================
        # ============================USUARIO=====================================
        # ========================================================================

        self.username_label = Label(self.root, text="Usuario ", bg="#a27114", fg="Black",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=75, y=155)

        self.username_entry = Entry(self.root, highlightthickness=0, relief=FLAT, bg="#D3D3D3", fg="#4f4e4d",
                                    font=("yu gothic ui semibold", 12))
        self.username_entry.place(x=75, y=188, width=380)  # trebuchet ms

        # ========================================================================
        # ===========================CONTRASEÑA===================================
        # ========================================================================

        self.password_label = Label(self.root, text="Contraseña ", bg="#a27114", fg="Black",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=75, y=240)

        self.password_entry = Entry(self.root, highlightthickness=0, relief=FLAT, bg="#D3D3D3", fg="#4f4e4d",
                                    font=("yu gothic ui semibold", 12))
        self.password_entry.place(x=75, y=274, width=380)

        # ========================================================================
        # ===========================BOTÓN GUARDAR================================
        # ========================================================================
        self.submit_button = Button(self.root, image=imagenes['new'], text=' GUARDAR ',
                                    font=("yu gothic ui", 13, "bold"), command=self.validation, compound="left")
        self.submit_button.image = imagenes['new']
        self.submit_button.place(x=60, y=320, width=120)

        # ========================================================================
        # ===========================BOTÓN INGRESAR===============================
        # ========================================================================
        self.login_button = Button(self.root, image=imagenes['login'], text=' INGRESAR ',
                                   font=("yu gothic ui", 13, "bold"), command=self.click_login, compound="left")
        self.login_button.image = imagenes['login']
        self.login_button.place(x=210, y=320, width=120)

        # ========================================================================
        # ============================BOTÓN SALIR=================================
        # ========================================================================
        self.exit_button = Button(self.root, image=imagenes['exit'], text=' SALIR ',
                                  font=("yu gothic ui", 13, "bold"), command=self.click_exit, compound="left")
        self.exit_button.image = imagenes['exit']
        self.exit_button.place(x=360, y=320, width=100)

    def slider(self):
        """
            Crea animación para el encabezado tomando el texto,
            y ese texto se llama después de cada 100 ms
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
            Configura la etiqueta de encabezado
            : return: cada 50 ms devuelve un nuevo color aleatorio.
        """
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(100, self.heading_color)

    def validation(self):
        """
            Validar las entradas para la creación del usuario administrador
        """
        obj_admin_database = database_connected.GetDatabase('use ddbb_sys_rest;')
        self.db_connection.create(obj_admin_database.get_database())

        if self.email_entry.get() == "":
            messagebox.showerror("SYST_CONTROL(IFAP®)-->(ERROR)", "POR FAVOR INGRESE SU EMAIL")
            self.email_entry.focus()

        elif self.username_entry.get() == "":
            messagebox.showerror("SYST_CONTROL(IFAP®)-->(ERROR)", "POR FAVOR INGRESE SU USUARIO")
            self.username_entry.focus()

        elif self.password_entry.get() == "":
            messagebox.showerror("SYST_CONTROL(IFAP®)-->(ERROR)", "POR FAVOR INGRESE SU CONTRASEÑA")
            self.password_entry.focus()

        else:
            try:
                obj_create_database = database_connected.GetDatabase('use ddbb_sys_rest;')
                self.db_connection.create(obj_create_database.get_database())
                self.tipo = 'Administrador'
                self.tipo_e = self.tipo

                obj_database_connected = database_connected.AdminData(self.username_entry.get(),
                                                                      self.email_entry.get(),
                                                                      self.password_entry.get(),
                                                                      self.tipo_e)
                query = 'insert into SEG_USUARIO (usuario, email, contrasena, tipo) values (%s, %s, %s, %s);'
                values = (obj_database_connected.get_username(), obj_database_connected.get_email(),
                          obj_database_connected.get_password(), obj_database_connected.get_tipo())

                self.db_connection.insert(query, values)
                messagebox.showinfo("SYST_CONTROL(REST®)-->(ÉXITO)", "USUARIO ADMIN AGREGADO CORRECTAMENTE")
                self.go_to_login()

            except BaseException as msg:
                messagebox.showerror("SYST_CONTROL(IFAP®)-->(ERROR!!!)", f"ERROR AL CONECTARSE AL SERVIDOR,\n"
                                                                         f"REVISE LA CONEXIÓN: {msg}")

    def click_login(self):
        """
           Cuando se hace clic en el botón de inicio de sesión,
           dirigirá a ese usuario al formulario de inicio de sesión
        """
        win = Toplevel()
        login_form.Login(win)
        self.root.withdraw()
        win.deiconify()

    def click_exit(self):
        ask = messagebox.askyesnocancel('SYST_CONTROL(IFAP®)-->(CERRAR SESIÓN)', 'CERRAR SYST_CONTROL(IFAP®)')
        if ask is True:
            self.root.quit()

    def go_to_login(self):
        """
            Cuando se hace clic en iniciar sesión, se abre el formulario de inicio de sesión
        """
        win = Toplevel()
        login_form.Login(win)
        self.root.withdraw()
        win.deiconify()


def root():
    root = tk.ThemedTk()
    root.get_themes()
    root.set_theme("arc")
    DatabaseConnected(root)
    root.mainloop()


if __name__ == '__main__':
    root()

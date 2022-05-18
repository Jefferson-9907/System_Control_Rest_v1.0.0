from tkinter import *
from ttkthemes import themed_tk as tk
import connet_database_1
import os
import login_form


class StartApp:
    """
        Comprobará si la base de datos ya está conectada, el formulario de inicio de sesión aparecerá
        de lo contrario le pedirá que conecte la base de datos llamando a la base de datos para la conexión.
    """

    def __init__(self, window):
        self.window = window
        self.window.geometry("0x0+0+0")
        self.window.title("SYST_CONTROL(REST®)-(INICIAR SESIÓN)")
        self.window.iconbitmap('recursos\\icon_rest.ico')
        self.window.resizable(False, False)

        self.len = os.path.getsize("database_data.txt")
        if self.len > 0:
            win = Toplevel()
            login_form.Login(win)
            self.window.withdraw()
            win.deiconify()

        elif self.len == 0:
            win = Toplevel()
            connet_database_1.ConnectDatabase(win)
            self.window.withdraw()
            win.deiconify()

        else:
            pass


def win():
    window = tk.ThemedTk()
    window.get_themes()
    window.set_theme("arc")
    StartApp(window)
    window.mainloop()


if __name__ == '__main__':
    win()

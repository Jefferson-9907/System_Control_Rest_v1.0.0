import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import random


class Table(tk.Frame):
    def __init__(
            self, parent=None, title="", headers=[],
            height=20, *args, **kwargs
    ):
        super().__init__(parent, *args, **kwargs)
        self._title = tk.Label(
            self, text=title, background="#F7F2E0", height=2, pady=5
        )
        self._headers = headers
        self._tree = ttk.Treeview(
            self, height=height, columns=self._headers, show="headings"
        )
        self._title.pack(side=tk.TOP, fill="x")

        # Agregamos dos scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(
            self, orient="horizontal", command=self._tree.xview
        )
        hsb.pack(side='bottom', fill='x')

        self._tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        self._tree.pack(side="left")

        for header in self._headers:
            self._tree.heading(header, text=header.title())
            self._tree.column(
                header, stretch=True,
                width=tkFont.Font().measure(header.title())
            )

    def add_row(self, row):
        self._tree.insert('', 'end', values=row)
        for i, item in enumerate(row):
            col_width = tkFont.Font().measure(item)
            if self._tree.column(self._headers[i], width=None) < col_width:
                self._tree.column(self._headers[i], width=col_width)

    def clear(self):
        self._tree.delete(*self._tree.get_children())


def consulta():
    for _ in range(random.randint(1, 13)):
        yield random.choices(range(1, 200), k=2)


def nueva_consulta():
    cursor = consulta()
    clientes_tab.clear()
    for row in cursor:
        clientes_tab.add_row(row)


t3 = tk.Tk()
clientes_headers = ["foo", "bar"]
clientes_tab = Table(
    t3, title="ENTRADAS DE MERCADERIAS", headers=clientes_headers
    )
clientes_tab.pack()
tk.Button(t3, text="Nueva consulta", command=nueva_consulta).pack()

t3.mainloop()

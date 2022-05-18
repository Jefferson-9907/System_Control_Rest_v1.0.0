import mysql.connector
import os
import pickle


class DatabaseConnection:
    """
        Conectando el front-end a la base de datos, aquí se escribe todo el código del backend, como insertar,
        actualizar, borrar, seleccionar
    """

    def __init__(self):
        # Frontend.connect_database.SaveDatabaseHost()
        self.file()

    def file(self):
        """
            Extrayendo las credenciales para la conexión al servidor como:
            host, puerto, nombre de usuario, contraseña que luego se utilizan para conectarse a la base de datos
        """

        self.len = os.path.getsize("./database_data.txt")
        if self.len > 0:
            f = open("./database_data.txt", "rb")
            self.dictcred = pickle.load(f)

            for k, p in self.dictcred.items():
                l = p[0]
                po = p[1]
                u = p[2]
                pa = p[3]
                self.d_connection(l, po, u, pa)

    def d_connection(self, host, port, username, password):
        """
            Tomando 4 argumentos funcionales el host es el dominio del servidor, el puerto es donde el servidor proxy
            reenvía,nombre de usuario es el nombre de usuario del host y la contraseña es la contraseña utilizada al
            configurar el usuario
        """
        self.connection = mysql.connector.connect(host=host, port=port, user=username, password=password)
        self.cursor = self.connection.cursor()

    def __del__(self):
        """
            Si la conexión se encuentra sin uso, esto cerrará de todos modos esa conexión
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

        except BaseException as msg:
            pass

    def create(self, query):
        """
            Utilizado para crear la base de datos en el host
        """
        self.cursor.execute(query)
        self.connection.commit()

    def search(self, query, values):
        """
            Buscar los valores de la base de datos
        """
        self.cursor.execute(query, values)
        data = self.cursor.fetchall()
        self.connection.commit()
        return data

    def insert(self, query, values):
        """
            Insertar valores desde la interfaz a la base de datos
        """
        self.cursor.execute(query, values)
        self.connection.commit()

    def select(self, query):
        """
            :returns data
        """
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.connection.commit()
        return data

    def update(self, query, values):
        """
            Actualiza los valores de la interfaz
        """
        self.cursor.execute(query, values)
        self.connection.commit()

    def delete(self, query, values):
        """
            Elimina los valores de la interfaz
        """
        self.cursor.execute(query, values)
        self.connection.commit()


DatabaseConnection()
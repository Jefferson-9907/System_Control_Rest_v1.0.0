class UsersRegistration:
    """
        Esta clase es una clase modelo para obtener valores del formulario de registro del estudiante y
        establecer todos los datos en la tabla de la base de datos backend llamada estudiantes
    """

    def __init__(self, usuario, email, contrasena, t_usuario):
        self.__usuario = usuario
        self.__email = email
        self.__contrasena = contrasena
        self.__t_usuario = t_usuario

    # ===========================set methods=======================

    def set_usuario(self, usuario):
        self.__usuario = usuario

    def set_email(self, email):
        self.__email = email

    def set_contrasena(self, contrasena):
        self.__contrasena = contrasena

    def set_t_usuario(self, t_usuario):
        self.__t_usuario = t_usuario

    # =====================get methods========================

    def get_usuario(self):
        return self.__usuario

    def get_email(self):
        return self.__email

    def get_contrasena(self):
        return self.__contrasena

    def get_t_usuario(self):
        return self.__t_usuario


class GetDatabase:
    def __init__(self, database):
        self.__database = database

    def get_database(self):
        return self.__database

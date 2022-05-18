class AuditoriaRegistration:
    """
        Esta clase es una clase modelo para obtener valores del formulario de registro del estudiante y
        establecer todos los datos en la tabla de la base de datos backend llamada estudiantes
    """

    def __init__(self, usuario, accion, fecha, hora):
        self.__usuario = usuario
        self.__accion = accion
        self.__fecha = fecha
        self.__hora = hora

    # ===========================set methods=======================

    def set_usuario(self, usuario):
        self.__usuario = usuario

    def set_accion(self, accion):
        self.__accion = accion

    def set_fecha(self, fecha):
        self.__fecha = fecha

    def set_hora(self, hora):
        self.__hora = hora

    # =====================get methods========================

    def get_usuario(self):
        return self.__usuario

    def get_accion(self):
        return self.__accion

    def get_fecha(self):
        return self.__fecha

    def get_hora(self):
        return self.__hora


class GetDatabase:
    def __init__(self, database):
        self.__database = database

    def get_database(self):
        return self.__database
